import logging
import random
from threading import Thread
import threading
import traceback
import queue
from typing import List
import os, sys, time, errno
from .objects import IpData
from .Routing import Routing
from .Rules import Rules
from .NetworkAdapter import NetworkAdapter

logging.basicConfig(level=logging.INFO)

class NetworkHookHandler:
    """
    """
    __mainThread = threading.current_thread
    
    # Create a queue to hold messages received from the pipe
    message_queue = queue.Queue()

    # Create a mutex to coordinate access to the queue
    message_mutex = threading.Lock()
    
    # Create a condition variable to notify waiting threads of new messages
    message_cond = threading.Condition(message_mutex)
    
    
    hookThreads: List[Thread] = []
    pipe_path = "/tmp/dru-hook"
    
    stopFlag = threading.Event()
    
    nics: List[str] = []
    nics_rt = {}
        
    def __init__(self, nics: List[str], nics_rt: dict) -> None:
        try:
            if not os.path.exists(self.pipe_path):
                os.mkfifo(path=self.pipe_path)
                os.chmod(self.pipe_path, mode=0o666)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                raise
        self.nics.extend(nics)
        self.nics_rt = nics_rt
                      
            
    def __openPipe(self) -> None:
        """_summary_"""
        logging.info(f"Opening pipe on {self.pipe_path}")
        with open(self.pipe_path, 'r') as fifo:
            while not self.stopFlag.is_set():
                content = fifo.read()
                lines = content.splitlines()
                if lines:
                    with self.message_mutex:
                        for line in lines:
                            message = line.strip()
                            if message and message in self.nics:
                                logging.info(f"DRUHook Received message from hook: {message}")
                                self.message_queue.put(message)
                            elif message == "stop":
                                logging.info(f"DRUHook Received fifo stop: {message}")
                                self.stopFlag.set()
                            else:
                                if len(message) > 0:
                                    logging.error(f"DRUHook is ignoring: {message} as it expects one of your predefined values or stop")
                        self.message_cond.notify_all()
                    with open(self.pipe_path, "w") as fifo_truncate:
                        logging.info("Truncating message cache")
                        fifo_truncate.write('')
                else:
                    time.sleep(1)
        logging.info(f"Pipe is closed!")


            
                
    def start(self) -> None:
        """Starts Thread that opens pipe and watches it for changes
        Returns:
            Thread: DruHookThread that has been started
        """
        _pthread = threading.Thread(target=self.__openPipe)
        self.hookThreads.append(_pthread)
        _pthread.start()
        for nic in self.nics:
            _hthread = threading.Thread(target=self.__onThreadStart, kwargs={'targetName': nic})
            self.hookThreads.append(_hthread)
            _hthread.start()
    
        
    def dryrun(self) -> None:
        """Runs all operations on defined interfaces
        """
        logging.info("DRUHook Dryrun started!\n")
        for nic in self.nics:
            self.__processMessage(nic)
        logging.info("\DRUHook Dryrun completed!\n")
        
    def stop(self) -> None:
        """
        """
        with open(self.pipe_path, 'w') as fifo:
            fifo.write('stop')
        self.stopFlag.set()
        for thread in self.hookThreads:
            thread.join()
        
    def __onThreadStart(self, targetName: str) -> None:
        """
        """
        if self.__mainThread == threading.current_thread():
            logging.error("DRUHook has not been started in a separete thread!")
            raise Exception("DRUHook is started in main thread!")
        logging.info(f"DRUHook Thread Started for {targetName}")
        
        while not self.stopFlag.is_set():
            with self.message_mutex:
                if self.message_queue.empty():
                    timeout = random.uniform(1, 5)
                    self.message_cond.wait(timeout)
                    continue                   
                    
                message = self.message_queue.get()
                if message == targetName:
                    logging.info(f"DRUHook Thread for {targetName} has received event")
                    self.__processMessage(message)
                else:
                    self.message_queue.put(message)
                 
    
    def __processMessage(self, nic: str) -> None:
        adapter = NetworkAdapter(nic)
        ipdata = adapter.getIpData()
        if (ipdata.isValid()):
            self.__routingTable_modify(ipdata)
        else:
            logging.info(f"Adding puller on {nic}")
            self.__puller_add(nic)
                
            
    def __routingTable_modify(self, ipdata: IpData) -> None:
        """_summary_
        """
        nic_rt_table = self.nics_rt[ipdata.name]
        logging.info(f"Modifying routing for {ipdata.name} on table {nic_rt_table}")
        
        Routing.flushRoutes(table=nic_rt_table) 
        Rules().flushRules(table=nic_rt_table)
        
        try:
            Routing("main").deleteRoutes(ipData=ipdata)
            
            
            rt = Routing(nic_rt_table)
            rt.deleteRoutes(ipData=ipdata)
            rt.addRoutes(ipData=ipdata)
            
            Rules().addRule(table=nic_rt_table, source=ipdata.ip)
        except Exception as e:
            traceback.print_exc()
        
            
    nicsPullerThreads: List[Thread] = []

    def __puller_add(self, nic: str) -> None:
        """Pulls on network adapter in seperate thread
        """
        waitTime: int = 60
        if len(list(filter(lambda x: x.name == nic, self.nicsPullerThreads))) != 0:
            logging.info(f"Found existing thread for {nic} skipping..")
            return
        thread = Thread(
            name=nic,
            target=self.__puller_thread,
            args=(nic,waitTime)
        )
        self.nicsPullerThreads.append(thread)
        thread.start()
        
    def __puller_remove(self, name: str) -> None:
        """Removes puller
        """
        try:
            if (len(self.nicsPullerThreads) > 0):
                targetThread = next(filter(lambda x: x.name == name, self.nicsPullerThreads))
                self.nicsPullerThreads.remove(targetThread)
        except Exception as e:
            traceback.print_exc()
    
    def __puller_thread(self, nic: str, waitTime: int = 60) -> None:
        """Thread for pulling on adapter
        """
        logging.info(f"Starting pulling on {nic}")
        
        isInInvalidState: bool = True
        while isInInvalidState or not self.stopFlag.is_set():
            time.sleep(waitTime)
            ipdata = NetworkAdapter(nic).getIpData()
            isInInvalidState = not ipdata.isValid()
            print(ipdata)
            if (isInInvalidState == False):
                self.__puller_remove(nic)
                self.__routingTable_modify(ipdata)
            else:
                logging.info(f"Pulling on {nic} in {waitTime}s")
        logging.info(f"Pulling on {nic} has ended")
        

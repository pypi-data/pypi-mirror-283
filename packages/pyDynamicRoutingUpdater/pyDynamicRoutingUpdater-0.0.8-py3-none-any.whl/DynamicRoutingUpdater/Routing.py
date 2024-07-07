from typing import List
import subprocess
import json
import sys, os
from .objects import Route, IpData
import logging
   
logging.basicConfig(level=logging.INFO)
    
def operationOut(command: str = None) -> None:
    result = os.system(command)
    if result != 0:
        logging.error(f"{command}\n\tResult: {result}")
    elif result == 512:
        logging.warn(f"{command}\n\tProvided the result: {result}")
    else:
        logging.info(f"{command}")

        

class Routing:
    """_summary_
    """
    table: str = None
    
    def __init__(self, table: str = None) -> None:
        """_summary_
        """
        if (table is None):
            raise ValueError(f"table is {table}, None is not supported!")
        self.table = table
        
    @staticmethod
    def getRoutes(table: str = None) -> List[Route]:
        """_summary_

        Returns:
            list[Route]: _description_
        """
        result: List[Route] = []
        
        try:
            query = f"ip -j route show table {table}" if table is not None and len(table) > 0 else "ip -j route show"
            data: List[dict[str, any]] = json.loads(subprocess.getoutput(query))
            
            for item in data:
                route = Route(
                    destination=item.get("dst"),
                    gateway=item.get("gateway"),
                    device=item.get("dev"),
                    preferredSource=item.get("prefsrc"),
                    scope=item.get("scope")
                )
                result.append(route)
        except json.JSONDecodeError:
            logging.error(f"No result for {query}")
            pass
        return result
    
    @staticmethod
    def flushRoutes(table: str = None) -> None:
        command = f"ip route flush table {table}"
        operationOut(command)
    
    @staticmethod
    def addRoute_Default(device: str, table: str = None) -> None:
        command = f"ip route add default dev {device} table {table}"
        operationOut(command)
        
    
    def addRoutes(self, ipData: IpData) -> None:
        """_summary_
        """       
        commands: List[str] = [
            "ip route add {}/{} dev {} src {} table {}".format(ipData.netmask, ipData.cidr, ipData.name, ipData.ip, self.table),
            "ip route add default via {} dev {} src {} table {}".format(ipData.gateway, ipData.name, ipData.ip, self.table),
            "ip route add {} dev {} src {} table {}".format(ipData.gateway, ipData.name, ipData.ip, self.table)
        ]
        for command in commands:
            operationOut(command)
    
    def deleteRoutes(self, ipData: IpData) -> None:
        commands: List[str] = [
            "ip route del {}/{} dev {} src {} table {}".format(ipData.netmask, ipData.cidr, ipData.name, ipData.ip, self.table),
            "ip route del default via {} dev {} src {} table {}".format(ipData.gateway, ipData.name, ipData.ip, self.table),
            "ip route del {} dev {} src {} table {}".format(ipData.gateway, ipData.name, ipData.ip, self.table)
        ]
        for command in commands:
            operationOut(command)
import threading
import socket
import logging
from datastructures.Assertion import Assertion

class AbstractJobRunner(threading.Thread):

    def __init__(self, approach:str, port:int):
        threading.Thread.__init__(self)
        self.approach = approach
        self.port = port
        self.server = None
    
    def _validateAssertion(self, assertion:Assertion):
        """
        Validate a single assertion.
        """
        # If not connected, connect to server
        if self.server == None:
            self._connect()
            
        # Send assertion in turtle format
        self.server.send(assertion.getTurtle().encode())
        
        # Receive score
        return self.server.recv(1024).decode()
    
    def _connect(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect(("127.0.0.1", self.port))
        except ConnectionRefusedError as ex:
            logging.warning("Cannot connect to approach '{}'".format(self.approach))
            raise(ex)
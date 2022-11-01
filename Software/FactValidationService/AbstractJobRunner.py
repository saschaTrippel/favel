import threading
import socket
import logging
import json
from datastructures.Assertion import Assertion

class AbstractJobRunner(threading.Thread):
    """
    Abstract class that implements basic functionality.
    Able to connect to a fact validation approach via TCP, send assertions in
    turtle format and receive their score.
    """

    def __init__(self, approach:str, port:int):
        threading.Thread.__init__(self)
        self.approach = approach
        self.port = port
        self.server = None
    
    def _validateAssertion(self, assertion:Assertion):
        """
        Validate a single assertion.
        """
            
        # Send assertion in turtle format
        self._send(assertion.getTurtle())
        
        # Receive score
        return self._receive()
    
    def _trainAssertion(self, assertion:Assertion):
        """
        Send the assertion to a supervised approach as training data.
        """
        self._send(json.dumps({"Assertion": assertion.getTurtle(), "Class": assertion.expectedScore}))
    
    def _connect(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect(("127.0.0.1", self.port))
        except ConnectionRefusedError as ex:
            logging.warning("Cannot connect to approach '{}'".format(self.approach))
            raise(ex)
        
    def _send(self, message:str):
        if self.server == None:
            self._connect()
        self.server.send(message.encode())
        
    def _receive(self):
        return self.server.recv(1024).decode()
    
    def unsupervised(self):
        return "unsupervised" in self._type()
        
    def _type(self):
        self._send("type")
        return self._receive()
    
    def trainingStart(self):
        self._send("training_start")
        return "train_start_ack" in self._receive()
    
    def trainingComplete(self):
        self._send("training_complete")

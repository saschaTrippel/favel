import json
from builtins import object

class Message:
    
    def __init__(self, type:str=None, content=None, subject:str=None, predicate:str=None, object:str=None, score=None, text:str=None):
        """
        Available types are:
            call    with content:
                - type
                - training_start
                - training_complete
            training with contents
        """
        if text != None:
            self.parse(text)
        else:
            self.type = type
            self.content = content
            self.subject = subject
            self.predicate = predicate
            self.object = object
            self.score = score
    
    def serialize(self):
        if type == call:
            return json.dumps({"type": self.type, "content": self.content})
        if type == training:
            return json.dumps({"type": self.type, "subject": self.subject, "predicate": self.predicate, "object": self.object, "score": self.score})
        if type == testing:
            return json.dumps({"type": self.type, "subject": self.subject, "predicate": self.predicate, "object": self.object})
    
    def parse(self, text:str):
        response = json.parse(text)
        self.type = response["type"]

        if self.type == "test_result":
            self.score = response["score"]
        elif self.type == "ack":
            self.content = response["content"]
        elif self.type == "type_response":
            self.content = response["content"]
        elif self.type == "error":
            self.content = response['content']


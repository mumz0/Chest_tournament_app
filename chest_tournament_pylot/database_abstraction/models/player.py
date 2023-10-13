import json
import os

from tinydb import TinyDB




class Player:

    def __init__(self, _first_name, _last_name, _birth_date, _score = None):
        self.first_name = _first_name
        self.last_name = _last_name
        self.birth_date = _birth_date
        self.score = _score


    def serialize(self):
        return {
            "first_name": self.first_name, 
            "last_name":  self.last_name,
            "birth_date": self.birth_date,
            "score": self.score
                }
    

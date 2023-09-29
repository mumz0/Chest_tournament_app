import os
from tinydb import Query, TinyDB
import json

from database_abstraction.models.database_helper import *

class Tournament:
    
    def __init__(self, name, location, start_date, description, tournament_number = None, end_date = None, rounds_number = 4, players = [], round_lst = []):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.description = description
        self.end_date = end_date
        self.round_number = rounds_number
        self.tournament_number = tournament_number
        self.players = players
        self.round_lst = round_lst
        self.tournament_db = TinyDB(os.getenv("TOURNAMENTS_DB_PATH"))


    def iterate_attributes(self):
        for attribute, value in self.__dict__.items():
            return value


    def serialize(self):
        return {
            "name": self.name, 
            "location": self.location,
            "start_date": self.start_date,
            "description": self.description,
            "end_date": None,
            "tournament_number": None,
            "round_number": 4,
            "players": self.players
            }
        
    
    @classmethod
    def deserialize(cls, data):
        return cls(
            name=data['name'],
            location=data['location'],
            start_date=data['start_date'],
            description=data['description'],
            end_date = None,
            tournament_number = None
            )




    

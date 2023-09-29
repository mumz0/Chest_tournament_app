import json
import os
from tinydb import Query, TinyDB


def save(obj, db):
    db.insert(obj)
    db.close()

def pull_database_obj_lst(db):
    print(db.all())
    return db.all()
    

def pull_database_obj(id, db):
    result = db.get(doc_id = id)
    result.doc_id
    return result

def update_obj(obj, db, attribute_value, attribute):
    db.update(obj, attribute == attribute_value)

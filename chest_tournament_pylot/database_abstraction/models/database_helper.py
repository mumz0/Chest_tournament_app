import json
import os
from tinydb import Query, TinyDB
from chest_tournament_pylot.database_abstraction.models.tournament import Tournament


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


# Fonction pour mettre à jour round_lst
def update_tournament_round(tournament_id, new_round_lst, db):
    tournament = db.get(doc_id = tournament_id)
    for round in new_round_lst:
        round_exist = False
        for round_db in tournament['round_lst']:
            if round['number'] == round_db['number']:
                round_exist = True
                continue
        if round_exist is False:
            tournament['round_lst'].append(round)
    db.update(tournament)



# Fonction pour mettre à jour round_lst
def update_match(tournament_id, round_number, new_match_lst, db):
    tournament = db.get(doc_id = tournament_id)
    for round in tournament['round_lst']:
        if round['number'] == round_number:
            tournament['round_lst'].round['match_lst'] = new_match_lst
    db.update(tournament)

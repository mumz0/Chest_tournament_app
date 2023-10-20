import json
import os
from tinydb import Query, TinyDB
from chest_tournament_pylot.database_abstraction.models.tournament import Tournament


def save(obj, db):
    db.insert(obj)

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
def update_tournament_round(tournament_id, round_serialized, db):

    tournament = db.get(doc_id = tournament_id)
    if len(tournament['round_lst']) == 0:
        tournament['round_lst'].append(round_serialized)
        db.update(tournament)
    else:
        for round in tournament['round_lst']:
            round_found = False
            if round['number'] == round_serialized['number']:
                round_found = True
        if round_found is False:
            tournament['round_lst'].append(round_serialized)
            db.update(tournament)



# Fonction pour mettre à jour round_lst
def update_match_and_player_score(tournament_id, round_number, new_match_lst, db):
    print('IN update_match_and_player_score')
    print("tournament_id", tournament_id)
    tournament = db.get(doc_id = tournament_id)
    tournament['round_lst'][round_number - 1]['match_lst'] = new_match_lst

    for player in tournament['players']:
        for match in new_match_lst:
            if player['player_id'] == match[0]['player_id']:
                player['score'] += match[0]['result']
                break
            if player['player_id'] == match[1]['player_id']:
                player['score'] += match[1]['result']
                break
    db.update(tournament)

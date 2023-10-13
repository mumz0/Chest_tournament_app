from tinydb import Query
from chest_tournament_pylot.database_abstraction.models.database_helper import *

class PlayerHelper():

    def check_player_in_db(player, db):
        is_already_exist = False
        player_lst = pull_database_obj_lst(db)
        for player_db in player_lst:
            if (
                player_db['first_name'] == player['first_name'] and
                player_db['last_name'] == player['last_name'] and  
                player_db['birth_date'] == player['birth_date']
            ):
                is_already_exist = True
                break 
        if not is_already_exist:
            print(player)
            save(player, db)
        return is_already_exist

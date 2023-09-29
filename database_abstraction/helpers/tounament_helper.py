from database_abstraction.models.database_helper import *
from database_abstraction.models.tournament import Tournament

class TournamentHelper():
    
    def add_player_to_tournament(self, player_id, player_db, tounament_id, tournament_db):
        tournament = pull_database_obj(tounament_id, tournament_db)
        print(tournament)
        player = pull_database_obj(player_id, player_db)
        print(player)
        is_already_exist = self.check_player_in_tournament_db(tournament, player_id)
        if not is_already_exist:
            tournament_db.update(tournament, tournament["players"].append({"player_id": player.doc_id, "score": 0}))
        else:
            print("ALREADY IN DB")


    def check_player_in_tournament_db(self, tournament, player_id):
        is_already_exist = False
        for player in tournament["players"]:
            if (player["player_id"] == player_id):
                is_already_exist = True
                break 
        return is_already_exist
    

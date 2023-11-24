import datetime
from chest_tournament_pylot.database_abstraction.models.database_helper import DatabaseHelper


class TournamentHelper():

    def add_player_to_tournament(self, player_id, player_db, tournament_id, tournament_db):
        tournament = DatabaseHelper.pull_database_obj(tournament_id, tournament_db)
        player = DatabaseHelper.pull_database_obj(player_id, player_db)

        # Vérifier si le joueur existe déjà dans le tournoi
        if not self.check_player_in_tournament_db(tournament, player_id):
            # Ajouter le joueur au tournoi
            player_info = {"player_id": player.doc_id, "score": 0}
            tournament["players"].append(player_info)
            tournament_db.update(tournament, doc_ids=[tournament.doc_id])

    def check_player_in_tournament_db(self, tournament, player_id):
        is_already_exist = False
        for player in tournament["players"]:
            if (player["player_id"] == player_id):
                is_already_exist = True
                break
        return is_already_exist

    def set_tournament_end_date(self):
        date_now = datetime.datetime.now()
        return date_now.strftime("%d/%m/%Y %H:%M:%S")

    def get_tournament_len(self, attr, db):
        tournament_lst = DatabaseHelper.pull_database_obj_lst(db)
        len_started_tournament_lst = []
        len_tournament_to_start_lst = []
        for tournament in tournament_lst:
            if tournament[attr] != [] and tournament['end_date'] is None:
                len_started_tournament_lst.append(tournament)
            if tournament[attr] == []:
                len_tournament_to_start_lst.append(tournament)
        return len(len_started_tournament_lst), len(len_tournament_to_start_lst), len(tournament_lst)

    def get_started_tournament_lst(self, attr, db):
        tournament_lst = DatabaseHelper.pull_database_obj_lst(db)
        len_tournament_lst = []
        for tournament in tournament_lst:
            if tournament[attr] != []:
                len_tournament_lst.append(tournament)

        return len_tournament_lst

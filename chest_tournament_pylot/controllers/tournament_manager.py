from chest_tournament_pylot.database_abstraction.helpers.round_helper import RoundHelper
from chest_tournament_pylot.database_abstraction.helpers.match_helper import MatchHelper
from chest_tournament_pylot.database_abstraction.helpers.tounament_helper import TournamentHelper
from chest_tournament_pylot.database_abstraction.models.round import Round
from chest_tournament_pylot.database_abstraction.models.tournament import Tournament
from chest_tournament_pylot.database_abstraction.models.database_helper import DatabaseHelper
from chest_tournament_pylot.views.view import View


class TournamentManager:

    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.view_obj = View()
        self.tournament = Tournament
        self.round = Round

    def create_tournament(self):
        ascii_art = self.view_obj.get_ascii_art("tournament_creation.txt")
        tournament_form_dict = self.view_obj.display_tournament_form(ascii_art)
        tournament = Tournament(
            tournament_form_dict["name"],
            tournament_form_dict["location"],
            tournament_form_dict["date"],
            tournament_form_dict["description"],
            )
        DatabaseHelper.save(tournament.serialize(), self.main_controller.tournament_db)
        self.main_controller.menu_manager.tournaments_manager()

    def show_tournaments_to_start(self):
        ascii_art = self.view_obj.get_ascii_art("start_tournament.txt")
        tournaments_lst = DatabaseHelper.pull_database_obj_lst(self.main_controller.tournament_db)
        back = {"0": {"value": self.main_controller.menu_manager.tournaments_manager, "text": "Retour"}}
        options = {}
        for tournament in tournaments_lst:
            if tournament["round_lst"] == []:
                options[str(tournament.doc_id)] = {
                    "name": tournament["name"],
                    "location": tournament["location"],
                    "date": tournament["start_date"],
                }
        response = self.view_obj.display_tournaments_list(options, ascii_art, back)
        if response == "0":
            self.main_controller.menu_manager.tournaments_manager()
        else:
            self.tournament_management(response)

    def show_all_tournaments(self):
        ascii_art = self.view_obj.get_ascii_art("all_tournament.txt")
        tournaments_lst = DatabaseHelper.pull_database_obj_lst(self.main_controller.tournament_db)
        back = {"0": {"value": self.main_controller.menu_manager.tournaments_manager, "text": "Retour"}}
        options = {}
        for tournament in tournaments_lst:
            options[str(tournament.doc_id)] = {
                "name": tournament["name"],
                "location": tournament["location"],
                "date": tournament["start_date"],
            }
        response = self.view_obj.display_tournaments_list(options, ascii_art, back)
        if response == "0":
            self.main_controller.menu_manager.tournaments_manager()
        else:
            self.tournament_management(response)

    def tournament_management(self, tournament_id=None, str=None):
        tournament = DatabaseHelper.pull_database_obj(tournament_id, self.main_controller.tournament_db)
        self.tournament = self.tournament.deserialize(tournament)
        ascii_art = self.view_obj.get_ascii_art("tournament_managment.txt")
        options = {
            "1": {"value": self.tournament_resumption, "text": "Reprendre le tournoi"} if str == "started"
            else {"value": self.start_tournament, "text": "Démarrer le tournoi"},
            "2": {"value": self.main_controller.player_manager.add_player_to_tournament_screen,
                  "text": "Ajouter un joueur"} if str != "started" else None,
            "3": {"value": self.main_controller.tournament_manager.classement_screen,
                  "text": "Classement"},
            "4": {"value": self.main_controller.tournament_manager.matches_history, "text": "Recap matchs"},
            "0": {"value": self.current_tournament, "text": "Retour"} if str == "started"
            else {"value": self.show_tournaments_to_start, "text": "Retour"},
        }
        response = self.view_obj.display_options(options, ascii_art)
        if response in options:
            option = options[response]
            if response == "0":
                option["value"]()
            elif response == "1" or response == "2" or response == "3" or response == "4":
                option["value"](tournament_id)
            else:
                self.main_controller.menu_manager.tournaments_manager()

    def current_tournament(self):
        ascii_art = self.view_obj.get_ascii_art("current_tournament.txt")
        tournaments_lst = TournamentHelper.get_started_tournament_lst(
            self, "round_lst", self.main_controller.tournament_db)
        back = {"0": {"value": self.main_controller.menu_manager.tournaments_manager, "text": "Retour"}}
        options = {}
        for tournament in tournaments_lst:
            if tournament["round_lst"] != [] and tournament['end_date'] is None:
                options[str(tournament.doc_id)] = {
                    "name": tournament["name"],
                    "location": tournament["location"],
                    "date": tournament["start_date"],
                }
        response = self.view_obj.display_tournaments_list(options, ascii_art, back)
        if response == "0":
            self.main_controller.menu_manager.tournaments_manager()
        else:
            self.tournament_management(response, "started")

    def start_tournament(self, tournament_id, index_start=1):
        for index in range(index_start, 5):
            self.round_process(index, tournament_id)
        tournament_helper_obj = TournamentHelper()
        self.tournament.end_date = tournament_helper_obj.set_tournament_end_date()
        DatabaseHelper.update_end_date_tournament(
            self.tournament.end_date, tournament_id, self.main_controller.tournament_db)
        self.main_controller.menu_manager.main_menu()

    def round_process(self, index, tournament_id):
        round_helper_obj = RoundHelper()
        match_helper_obj = MatchHelper()
        round_obj = Round(
            number=str(index),
            start_timestamp=round_helper_obj.set_round_time(),
            end_timestamp=None,
            match_lst=match_helper_obj.create_match_lst(
                self.tournament.players, self.tournament.round_lst
                ))
        self.tournament.round_lst.append(round_obj)
        round_serialized = self.round.serialize(round_obj)
        DatabaseHelper.update_tournament_round(
            tournament_id, round_serialized, self.main_controller.tournament_db)
        self.match_process(index, round_obj.match_lst, tournament_id)
        round_obj.end_timestamp = round_helper_obj.set_round_time()
        DatabaseHelper.update_end_time_round(
            round_obj.end_timestamp, round_obj.number, tournament_id, self.main_controller.tournament_db)

    def match_process(self, index, match_lst, tournament_id):
        for match in match_lst:
            result_match = self.set_results_matches(index, match)
            DatabaseHelper.update_match_and_player_score(
                str(tournament_id), index, result_match, self.main_controller.tournament_db)

    def result_match_page(self, index_round, match, player_obj_1, player_obj_2):
        ascii_art = self.view_obj.get_ascii_art("matchs_results.txt")
        response = self.view_obj.display_result_match(index_round, player_obj_1, player_obj_2, ascii_art)
        if response == "1":
            match[0]['result'] = 1
            match[1]['result'] = 0
        elif response == "2":
            match[0]['result'] = 0
            match[1]['result'] = 1
        elif response == "3":
            match[0]['result'] = 0.5
            match[1]['result'] = 0.5
        elif response == "0":
            self.main_controller.menu_manager.main_menu()
        return match

    def tournament_resumption(self, tournament_id):
        new_match_lst = []
        tournament = DatabaseHelper.pull_database_obj(tournament_id, self.main_controller.tournament_db)
        for round in tournament["round_lst"]:
            for match in round["match_lst"]:
                if match[0]['result'] is None and match[1]['result'] is None:
                    new_match_lst.append(match)
            self.match_process(round['number'], new_match_lst, tournament_id)
            round_helper_obj = RoundHelper()
            round["end_timestamp"] = round_helper_obj.set_round_time()
            DatabaseHelper.update_end_time_round(
                round["end_timestamp"], round["number"], tournament_id, self.main_controller.tournament_db)
        self.start_tournament(tournament_id, int(round["number"]) + 1)

    def set_results_matches(self, round_number, match):
        players_in_match = []
        for player in match:
            player_obj = DatabaseHelper.pull_database_obj(int(player['player_id']), self.main_controller.player_db)
            players_in_match.append(player_obj)
        result_match = self.result_match_page(round_number, match, players_in_match[0], players_in_match[1])
        players_in_match.clear()
        return result_match

    def classement_screen(self, tournament_id):
        ascii_art = self.view_obj.get_ascii_art("ranking.txt")
        player_ranking_lst = []
        players = DatabaseHelper.pull_tournament_attr("players", tournament_id, self.main_controller.tournament_db)
        sorted_players_ranking_list = sorted(players, key=lambda x: x['score'], reverse=True)
        for player in sorted_players_ranking_list:
            player_obj = DatabaseHelper.pull_database_obj(player['player_id'], self.main_controller.player_db)
            new_player_obj = {
                'first_name': player_obj['first_name'],
                'last_name': player_obj['last_name'],
                'score': player['score']
                }
            player_ranking_lst.append(new_player_obj)
            back = {"0": {"text": "Retour"}}
        response = self.view_obj.display_tournament_ranks(player_ranking_lst, ascii_art, back)
        if response == "0":
            self.main_controller.menu_manager.tournaments_manager()

    def matches_history(self, tournament_id):
        ascii_art = self.view_obj.get_ascii_art("match_history.txt")
        new_round_lst = []
        round_lst = DatabaseHelper.pull_tournament_attr("round_lst", tournament_id, self.main_controller.tournament_db)
        for round in round_lst:
            new_match_lst = []
            for match in round['match_lst']:
                player_objs_lst = DatabaseHelper.pull_database_lst(
                    [match[0]['player_id'], match[1]['player_id']], self.main_controller.player_db)
                new_match_lst.append({
                    'first_name1': player_objs_lst[0]["first_name"],
                    'last_name1': player_objs_lst[0]["last_name"],
                    "score1": match[0]['result'],
                    'first_name2': player_objs_lst[1]["first_name"],
                    'last_name2': player_objs_lst[1]["last_name"],
                    "score2": match[1]['result']
                    })
            new_round_lst.append({"round_number": round['number'], "match_lst": new_match_lst})
        back = {"0": {"text": "Retour"}}
        response = self.view_obj.display_tournament_matches_history(new_round_lst, ascii_art, back)
        if response == "0":
            self.main_controller.menu_manager.tournaments_manager()

from chest_tournament_pylot.database_abstraction.helpers.tounament_helper import TournamentHelper
from chest_tournament_pylot.database_abstraction.models.player import Player
from chest_tournament_pylot.database_abstraction.models.tournament import Tournament
from chest_tournament_pylot.views.view import View


class MenuManager:

    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.view_obj = View()
        self.player = Player
        self.tournament = Tournament

    def main_menu(self):
        ascii_art = self.view_obj.get_ascii_art("chest_pylot_title.txt")
        options = {
            "1": {"value": self.tournaments_manager, "text": "Gestion des tournois"},
            "2": {"value": self.players_manager, "text": "Gestion des joueurs"},
            "3": {"value": self.close_app, "text": "Quitter"}
        }

        response = self.view_obj.display_options(options, ascii_art)
        options[response]["value"]()

    def tournaments_manager(self):
        TournamentHelper_obj = TournamentHelper()
        len_started_tournaments, len_tournaments_to_start, len_tournaments = TournamentHelper_obj.get_tournament_len(
            "round_lst", self.main_controller.tournament_db)
        ascii_art = self.view_obj.get_ascii_art("tournament_managment_title.txt")
        options = {
            "1": {"value": self.main_controller.tournament_manager.create_tournament,
                  "text": "Creer un tournoi"},
            "2": {"value": self.main_controller.tournament_manager.current_tournament,
                  "text": f"Tournois en cours[{len_started_tournaments}]"},
            "3": {"value": self.main_controller.tournament_manager.show_tournaments_to_start,
                  "text": f"Débuter un tournoi[{len_tournaments_to_start}]"},
            "4": {"value": self.main_controller.tournament_manager.show_all_tournaments,
                  "text": f"Afficher tous les tournois[{len_tournaments}]"},
            "0": {"value": self.main_menu, "text": "Retour"}
        }
        response = self.view_obj.display_options(options, ascii_art)
        options[response]["value"]()

    def players_manager(self):
        ascii_art = self.view_obj.get_ascii_art("players_managment_title.txt")
        options = {
            "1": {"value": self.main_controller.player_manager.show_all_players, "text": "Afficher tous les joueurs"},
            "2": {"value": self.main_controller.player_manager.create_player, "text": "Creer un joueur"},
            "3": {"value": self.tournaments_manager, "text": "Retour"}
        }
        response = self.view_obj.display_options(options, ascii_art)
        options[response]["value"]()

    def errors_manager(self, message):
        ascii_art = self.view_obj.get_ascii_art("error.txt")
        options = {
            "1": {"value": None, "text": message},
            "0": {"value": self.main_menu, "text": "Retour"}
        }
        response = self.view_obj.display_options(options, ascii_art)
        options[response]["value"]()

    def close_app(self):
        self.view_obj.display_end_message()
        return

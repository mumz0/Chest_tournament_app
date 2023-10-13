from chest_tournament_pylot.database_abstraction.models.player import Player
from chest_tournament_pylot.database_abstraction.models.tournament import Tournament
from chest_tournament_pylot.views.view import View
from chest_tournament_pylot.database_abstraction.models.database_helper import *
from chest_tournament_pylot.database_abstraction.helpers.player_helper import PlayerHelper
from chest_tournament_pylot.database_abstraction.helpers.tounament_helper import TournamentHelper


class PlayerManager:
    
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.view_obj = View()
        self.player = Player
        self.tournament = Tournament


    def show_all_players(self):
        ascii_art = """
    ______                    __               _                                 
   /_  __/___  __  _______   / /__  _____     (_)___  __  _____  __  ____________
    / / / __ \/ / / / ___/  / / _ \/ ___/    / / __ \/ / / / _ \/ / / / ___/ ___/
   / / / /_/ / /_/ (__  )  / /  __(__  )    / / /_/ / /_/ /  __/ /_/ / /  (__  ) 
  /_/  \____/\__,_/____/  /_/\___/____/  __/ /\____/\__,_/\___/\__,_/_/  /____/  
                                        /___/                                    
"""
        players_lst = pull_database_obj_lst(self.main_controller.player_db)
        
        options = {}
        back = {"0": {"value":self.main_controller.menu_manager.tournaments_manager, "text": "Retour"}}

        for player in players_lst:
            options[str(player.doc_id)] = {
                "first_name": player["first_name"], "last_name": player["last_name"] , "birth_date": player["birth_date"]
            }
        response = self.view_obj.display_players_list(options, ascii_art, back)
        options[response]["value"]()


    def create_player(self):
        ascii_art = """
     ______      __        __  _                  _                            
    / ____/_____/_/ ____ _/ /_(_)___  ____       (_)___  __  _____  __  _______
   / /   / ___/ _ \/ __ `/ __/ / __ \/ __ \     / / __ \/ / / / _ \/ / / / ___/
  / /___/ /  /  __/ /_/ / /_/ / /_/ / / / /    / / /_/ / /_/ /  __/ /_/ / /    
  \____/_/   \___/\__,_/\__/_/\____/_/ /_/  __/ /\____/\__,_/\___/\__,_/_/     
                                           /___/                               
"""   

        players_form_dict = self.view_obj.display_player_form(ascii_art)

        is_already_in_db = PlayerHelper.check_player_in_db(players_form_dict, self.main_controller.player_db)
        if not is_already_in_db:
            player = Player(
                players_form_dict["first_name"],
                players_form_dict["last_name"],
                players_form_dict["birth_date"],
                )
        if is_already_in_db == True:
            message = "Le joueur éxiste déjà dans la base de donnée"
            self.main_controller.menu_manager.errors_manager(message)
        else:
            self.main_controller.menu_manager.players_manager()


    def add_player_to_tournament_screen(self, tournament_id):
        
        players_lst = pull_database_obj_lst(self.main_controller.player_db)
        ascii_art = """
      ___      _             __                                _                            
     /   |    (_)___  __  __/ /____  _____   __  ______       (_)___  __  _____  __  _______
    / /| |   / / __ \/ / / / __/ _ \/ ___/  / / / / __ \     / / __ \/ / / / _ \/ / / / ___/
   / ___ |  / / /_/ / /_/ / /_/  __/ /     / /_/ / / / /    / / /_/ / /_/ /  __/ /_/ / /    
  /_/  |_|_/ /\____/\__,_/\__/\___/_/      \__,_/_/ /_/  __/ /\____/\__,_/\___/\__,_/_/     
        /___/                                           /___/                               
"""
        options = {}
        options["0"] = {
                "value": self.main_controller.tournament_manager.show_all_tournaments, "text": "Retour"
            }
        for player in players_lst:
            options[str(player.doc_id)] = {
                "text": player["first_name"] + player["last_name"] + player["birth_date"]
            }
        response = self.view_obj.display_options(options, ascii_art)

        if response != "0":
            Tournament_helper_obj = TournamentHelper()
            Tournament_helper_obj.add_player_to_tournament(response, self.main_controller.player_db, tournament_id, self.main_controller.tournament_db)
            self.main_controller.tournament_manager.tournament_management(tournament_id)
        else:
             options[response]["value"]()
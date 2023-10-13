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
        ascii_art = """
         ________              __     ____        __      __    
        / ____/ /_  ___  _____/ /_   / __ \__  __/ /___  / /_   
       / /   / __ \/ _ \/ ___/ __/  / /_/ / / / / / __ \/ __/   
      / /___/ / / /  __(__  ) /_   / ____/ /_/ / / /_/ / /_     
 _____\____/_/ /_/\___/____/\__/  /_/    \__, /_/\____/\__/_____
/_____/                                 /____/           /_____/
"""
        options = {
            "1": {"value": self.tournaments_manager, "text": "Gestion des tournois"},
            "2": {"value": self.players_manager, "text": "Gestion des joueurs"},
            "3": {"value": "fonction quitter", "text": "Quitter"}
        }

        response = self.view_obj.display_options(options, ascii_art)
        options[response]["value"]()


    def tournaments_manager(self):
        
        ascii_art = """
   ______          __  _                    __             __                               _     
  / ____/__  _____/ /_(_)___  ____     ____/ /__  _____   / /_____  __  ___________  ____  (_)____
 / / __/ _ \/ ___/ __/ / __ \/ __ \   / __  / _ \/ ___/  / __/ __ \/ / / / ___/ __ \/ __ \/ / ___/
/ /_/ /  __(__  ) /_/ / /_/ / / / /  / /_/ /  __(__  )  / /_/ /_/ / /_/ / /  / / / / /_/ / (__  ) 
\____/\___/____/\__/_/\____/_/ /_/   \__,_/\___/____/   \__/\____/\__,_/_/  /_/ /_/\____/_/____/  
                                                                                                  
"""    
        options = {
            "1": {"value": self.main_controller.tournament_manager.create_tournament, "text": "Creer un tournoi"},
            "2": {"value": self.main_controller.tournament_manager.current_tournament, "text": "Reprendre le tournoi en cours"},
            "3": {"value": self.main_controller.tournament_manager.show_all_tournaments, "text": "Afficher tous les tournois"},
            "4": {"value": self.main_menu, "text": "Retour"}
        }
        response = self.view_obj.display_options(options, ascii_art)
        options[response]["value"]()


    def players_manager(self):
        ascii_art = """
   ______          __  _                    __               _                                 
  / ____/__  _____/ /_(_)___  ____     ____/ /__  _____     (_)___  __  _____  __  ____________
 / / __/ _ \/ ___/ __/ / __ \/ __ \   / __  / _ \/ ___/    / / __ \/ / / / _ \/ / / / ___/ ___/
/ /_/ /  __(__  ) /_/ / /_/ / / / /  / /_/ /  __(__  )    / / /_/ / /_/ /  __/ /_/ / /  (__  ) 
\____/\___/____/\__/_/\____/_/ /_/   \__,_/\___/____/  __/ /\____/\__,_/\___/\__,_/_/  /____/  
                                                      /___/                                    
"""
        options = {
            "1": {"value": self.main_controller.player_manager.show_all_players, "text": "Afficher tous les joueurs"},
            "2": {"value": self.main_controller.player_manager.create_player, "text": "Creer un joueur"},
            "3": {"value": self.tournaments_manager, "text": "Retour"}
        }
        response = self.view_obj.display_options(options, ascii_art)
        options[response]["value"]()



    def errors_manager(self, message):
        ascii_art = """
      ______                    
     / ____/_____________  _____
    / __/ / ___/ ___/ __ \/ ___/
   / /___/ /  / /  / /_/ / /    
  /_____/_/  /_/   \____/_/     
                                
"""

        options = {
            "1": {"value": None, "text": message},
            "0": {"value": self.main_menu, "text": "Retour"}
        }
        response = self.view_obj.display_options(options, ascii_art)
        options[response]["value"]()
    


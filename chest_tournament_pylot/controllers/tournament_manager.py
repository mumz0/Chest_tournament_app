from database_abstraction.helpers.round_helper import RoundHelper
from database_abstraction.models.round import Round
from database_abstraction.models.tournament import Tournament
from database_abstraction.models.database_helper import *
from chest_tournament_pylot.views.view import View


class TournamentManager:

    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.view_obj = View()
        self.tournament = Tournament
        self.round = Round


    def create_tournament(self):
        ascii_art = """
     ______      __        __  _                    __         __                               _ 
    / ____/_____/_/ ____ _/ /_(_)___  ____     ____/ /_  __   / /_____  __  ___________  ____  (_)
   / /   / ___/ _ \/ __ `/ __/ / __ \/ __ \   / __  / / / /  / __/ __ \/ / / / ___/ __ \/ __ \/ / 
  / /___/ /  /  __/ /_/ / /_/ / /_/ / / / /  / /_/ / /_/ /  / /_/ /_/ / /_/ / /  / / / / /_/ / /  
  \____/_/   \___/\__,_/\__/_/\____/_/ /_/   \__,_/\__,_/   \__/\____/\__,_/_/  /_/ /_/\____/_/   
                                                                                                  
"""     

        tournament_form_dict = self.view_obj.display_tournament_form(ascii_art)

        tournament = Tournament(

            tournament_form_dict["name"],
            tournament_form_dict["location"],
            tournament_form_dict["date"],
            tournament_form_dict["description"],
            )

        tournament.save()
        self.main_controller.menu_manager.tournaments_manager()

    
    def show_all_tournaments(self):
        
        ascii_art = """
    ______                    __             __                               _     
   /_  __/___  __  _______   / /__  _____   / /_____  __  ___________  ____  (_)____
    / / / __ \/ / / / ___/  / / _ \/ ___/  / __/ __ \/ / / / ___/ __ \/ __ \/ / ___/
   / / / /_/ / /_/ (__  )  / /  __(__  )  / /_/ /_/ / /_/ / /  / / / / /_/ / (__  ) 
  /_/  \____/\__,_/____/  /_/\___/____/   \__/\____/\__,_/_/  /_/ /_/\____/_/____/  
                                                                                    
"""
        tournaments_lst = pull_database_obj_lst(self.main_controller.tournament_db)
        back = {"0": {"value":self.main_controller.menu_manager.tournaments_manager, "text": "Retour"}}
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

        

    def tournament_management(self, tournament_id= None):

        tournament = pull_database_obj(tournament_id, self.main_controller.tournament_db)
        self.tournament.deserialize(tournament)
        print(self.tournament)

        self.tournament = self.tournament.deserialize(tournament)

        ascii_art = """
     ______          __  _                    __         __                               _ 
    / ____/__  _____/ /_(_)___  ____     ____/ /_  __   / /_____  __  ___________  ____  (_)
   / / __/ _ \/ ___/ __/ / __ \/ __ \   / __  / / / /  / __/ __ \/ / / / ___/ __ \/ __ \/ / 
  / /_/ /  __(__  ) /_/ / /_/ / / / /  / /_/ / /_/ /  / /_/ /_/ / /_/ / /  / / / / /_/ / /  
  \____/\___/____/\__/_/\____/_/ /_/   \__,_/\__,_/   \__/\____/\__,_/_/  /_/ /_/\____/_/   
                                                                                            
"""
        options = {
            "1": {"value": self.start_tournament, "text": "Démarrer le tournoi"},
            "2": {"value": self.main_controller.player_manager.add_player_to_tournament_screen, "text": "Ajouter un joueur"},
            "3": {"value": self.show_all_tournaments, "text": "Retour"}
        }
        response = self.view_obj.display_options(options, ascii_art)
        if response == "2":
            options[response]["value"](tournament_id)
        else:
            options[response]["value"]()


    def current_tournament(self):
        print("JE REPRENDS LE TOURNOI EN COURS")


    def start_tournament(self):
        print(self.tournament.start_date)
        round_helper_obj = RoundHelper()
        time_snapshot = round_helper_obj.set_round_time()
        self.round.get_start_timestamp = time_snapshot
        print(self.round.get_start_timestamp)
        for round_number in self.tournament.rounds_number:
            self.round_process()


    def round_process(self):
        player_lst = self.tournament.players
        print(player_lst)
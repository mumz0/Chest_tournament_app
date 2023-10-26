from chest_tournament_pylot.database_abstraction.helpers.round_helper import RoundHelper
from chest_tournament_pylot.database_abstraction.helpers.match_helper import MatchHelper
from chest_tournament_pylot.database_abstraction.helpers.tounament_helper import TournamentHelper
from chest_tournament_pylot.database_abstraction.models.round import Round
from chest_tournament_pylot.database_abstraction.models.tournament import Tournament
from chest_tournament_pylot.database_abstraction.models.database_helper import *
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

        save(self.tournament.serialize(tournament), self.main_controller.tournament_db)
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
            if tournament["round_lst"] != []:
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
        if response == "2" or response == "1":
            options[response]["value"](tournament_id)
        else:
            options[response]["value"]()


    def current_tournament(self):
        print("JE REPRENDS LE TOURNOI EN COURS")


    def start_tournament(self, tournament_id):
        for index in range(1, 5):
            print("round", index)
            # print("round_lst", self.tournament.round_lst)
            self.round_process(index, tournament_id)
        # self.tournament.end_date = TournamentHelper.set_tournament_end_date()

    def round_process(self, index, tournament_id):
        round_helper_obj = RoundHelper()
        match_helper_obj = MatchHelper()
        round_obj = Round(
            number = str(index), 
            start_timestamp = round_helper_obj.set_round_time(), 
            end_timestamp = None, 
            match_lst = match_helper_obj.create_match_lst(self.tournament.players, self.tournament.round_lst))

        self.tournament.round_lst.append(round_obj)
        print('self.tournament.round_lst', self.tournament.round_lst)
        
        round_serialized = self.round.serialize(round_obj)
        update_tournament_round(tournament_id, round_serialized, self.main_controller.tournament_db)

        player_in_match = []
        for match in round_obj.match_lst:
            for player in match:
                player_obj = pull_database_obj(int(player['player_id']), self.main_controller.player_db)
                player_in_match.append(player_obj)
                # print(player_in_match)
            match = self.result_match_page(index, match, player_in_match[0], player_in_match[1])
            player_in_match.clear()
        round_obj.end_timestamp = round_helper_obj.set_round_time()
        update_match_and_player_score(str(tournament_id), index, round_obj.match_lst, self.main_controller.tournament_db)
        

        

    

    def result_match_page(self, index_round, match, player_obj_1, player_obj_2):
        ascii_art = """
      __  ___      __       __                                 ____      
     /  |/  /___ _/ /______/ /_  _____   ________  _______  __/ / /______
    / /|_/ / __ `/ __/ ___/ __ \/ ___/  / ___/ _ \/ ___/ / / / / __/ ___/
   / /  / / /_/ / /_/ /__/ / / (__  )  / /  /  __(__  ) /_/ / / /_(__  ) 
  /_/  /_/\__,_/\__/\___/_/ /_/____/  /_/   \___/____/\__,_/_/\__/____/  
                                                                         
"""
        response = self.view_obj.display_result_match(index_round, player_obj_1, player_obj_2, ascii_art)
        if response == "1":
            match[0]['result'] = 1
            match[1]['result'] = 0
        elif response == "2":
            match[0]['result'] = 0
            match[1]['result'] = 1
        else:
            match[0]['result'] = 0.5
            match[1]['result'] = 0.5
        return match

    
    def get_started_tournament_len(self):
        tournament_lst = pull_database_obj_lst(self.main_controller.tournament_db)
        started_tournament_lst = []
        for tournament in tournament_lst:
            if tournament["round_lst"] != []:
                started_tournament_lst.append(tournament) 
        return len(started_tournament_lst)
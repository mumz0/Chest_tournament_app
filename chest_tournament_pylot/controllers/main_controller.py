import os
from tinydb import TinyDB
from chest_tournament_pylot.controllers.player_manager import PlayerManager
from chest_tournament_pylot.controllers.tournament_manager import TournamentManager
from chest_tournament_pylot.controllers.menu_manager import MenuManager


class MainController:

    def __init__(self):
        self.player_manager = PlayerManager(self)
        self.menu_manager = MenuManager(self)
        self.tournament_manager = TournamentManager(self)
        self.tournament_db = TinyDB(os.getenv("TOURNAMENTS_DB_PATH"))
        self.player_db = TinyDB(os.getenv("PLAYERS_DB_PATH"))

    def run_app(self):
        self.menu_manager.main_menu()

import os
from tinydb import TinyDB, Query
from chest_tournament_pylot.controllers.main_controller import MainController
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    
    main_controller = MainController()
    main_controller.run_app()
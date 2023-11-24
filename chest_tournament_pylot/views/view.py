import os


class View:

    def __init__(self):
        pass

    def display_options(self, options, ascii_art):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_art)
        print("")
        print("")
        for index, option in options.items():
            if option and option.get("text") is not None:
                print(index, option["text"])

        response = input("Votre choix: ")
        if response in options:
            return response
        return self.display_options(options, ascii_art)

    def display_tournament_form(self, ascii_art):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_art)
        print("")
        print("")
        options_form_dict = {
            "name": input("Nom: "),
            "location": input("Lieu: "),
            "date": input("Date (DD/MM/YYYY): "),
            "description": input("Description : ")
            }
        return options_form_dict

    def display_tournaments_list(self, tournaments_list, ascii_art, back):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_art)
        print("")
        print("")
        for index in tournaments_list:
            print(index, tournaments_list[index]["name"], tournaments_list[index]["location"], tournaments_list[index]["date"])
        for index in back:
            print(index, back[index]["text"])
        response = input("Votre choix: ")
        if response in tournaments_list:
            return response
        elif response in back:
            return response
        else:
            return self.display_tournaments_list(tournaments_list, ascii_art, back)

    def display_players_list(self, players, ascii_art, menu):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_art)
        print("")
        print("")
        for index in menu:
            print(index, menu[index]["text"])
        for index in players:
            print(index, players[index]["first_name"], players[index]["last_name"], players[index]["birth_date"])

        response = input("Votre choix: ")
        if response in players:
            return response
        if response in menu:
            return response
        else:
            return self.display_players_list(players, ascii_art, menu)

    def display_tournament_ranks(self, players, ascii_art, back):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_art)
        print("")
        print("")
        for index, player in enumerate(players, start=1):
            if index == 1:
                print(f"WINNER {player['first_name']} {player['last_name']}: {player['score']} pts")
            else:
                print(f"{index}th {player['first_name']} {player['last_name']}: {player['score']} pts")
        print("")
        print(list(back.keys())[0], back["0"]["text"])
        return input("Votre choix: ")

    def display_tournament_matches_history(self, round_lst, ascii_art, back):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_art)
        print("")
        print("")
        for round in round_lst:
            print("")
            print("Round", round['round_number'])
            for match in round['match_lst']:
                if match['score1'] == 1:
                    print(f"{match['first_name1']} {match['last_name1']}  GAGNE CONTRE  {match['first_name2']} {match['last_name2']}")
                elif match['score1'] == 0:
                    print(f"{match['first_name2']} {match['last_name2']}  GAGNE CONTRE  {match['first_name1']} {match['last_name1']}")
                else:
                    print(f"{match['first_name1']} {match['last_name1']}  EGALITE CONTRE  {match['first_name2']} {match['last_name2']}")
        print("")
        print(list(back.keys())[0], back["0"]["text"])
        return input("Votre choix: ")

    def display_player_form(self, ascii_art):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_art)
        print("")
        print("")
        options_form_dict = {
            "first_name": input("First name: "),
            "last_name": input("Last name: "),
            "birth_date": input("Birth date (DD/MM/YYYY): ")
            }
        return options_form_dict

    def display_error_message(self, message):
        print(message)

    def display_result_match(self, index_round, player_obj_1, player_obj_2, ascii_art):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_art)
        print('ROUND ', index_round, ":")
        print("")
        print("1: ", player_obj_1['last_name'], player_obj_1['first_name'])
        print("2: ", player_obj_2['last_name'], player_obj_2['first_name'])
        print("3: ", "Match null")
        print("")
        print("0: Menu Principal")
        response = input("Résultat: ")
        return response

    def display_end_message(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("FERMETURE DE _CHEST PYLOT")

    def get_ascii_art(self, ascii_art_name_str):
        with open("chest_tournament_pylot/views/ascii_arts/" + ascii_art_name_str, "r") as file:
            ascii_art = file.read()
        return ascii_art

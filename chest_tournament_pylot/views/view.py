import os


class View:
    
    def __init__(self):
        pass

    def display_options(self, options, ascii_art):
        os.system('cls')
        print(ascii_art)
        print("")
        print("")
        for index in options:
            print(index, options[index]["text"])

        response = input("Votre choix: ")
        if response in options:
            return response
        return self.display_options(options, ascii_art)
    

    def display_tournament_form(self, ascii_art):
        os.system('cls')
        print(ascii_art)
        print("")
        print("")
        options_form_dict = {
            "name": input(f"Nom: "), 
            "location": input(f"Lieu: "), 
            "date": input(f"Date (DD/MM/YYYY): "),
            "description": input(f"Description : ")
            }
        return options_form_dict


    def display_tournaments_list(self, tournaments_list, ascii_art, back):
        os.system('cls')
        print(ascii_art)
        print("")
        print("")
        for index in back:
            print(index, back[index]["text"])
        for index in tournaments_list:
            print(index, tournaments_list[index]["name"], tournaments_list[index]["location"], tournaments_list[index]["date"])

        response = input("Votre choix: ")
        if response in tournaments_list:
            return response
        elif response in back:
            return response
        else:
            return self.display_tournaments_list(tournaments_list, ascii_art, back)
        

    def display_players_list(self, options, ascii_art, previous):
        os.system('cls')
        print(ascii_art)
        print("")
        print("")
        
        for index in previous:
            print(index, previous[index]["text"])
        for index in options:
            print(index, options[index]["first_name"], options[index]["last_name"], options[index]["birth_date"])

        response = input("Votre choix: ")
        if response in options:
            return previous
        if response in previous:
            return response
        else:
            return self.display_players_list(options, ascii_art)
        


    def display_player_form(self, ascii_art):
        os.system('cls')
        print(ascii_art)
        print("")
        print("")
        options_form_dict = {
            "first_name": input(f"First name: "), 
            "last_name": input(f"Last name: "), 
            "birth_date": input(f"Birth date (DD/MM/YYYY): ")
            }
        return options_form_dict
    

    def display_error_message(self, message):
        print(message)

    

    def display_result_match(self, index_round, player_obj_1, player_obj_2, ascii_art):
        # print(player_obj_1['last_name'], player_obj_1['first_name'], " VS ", player_obj_2['last_name'], player_obj_2['first_name'])
        # os.system('cls')
        print(ascii_art)
        print('ROUND ', index_round, ":")
        print("")
        print("1: ", player_obj_1['last_name'], player_obj_1['first_name'])
        print("2: ", player_obj_2['last_name'], player_obj_2['first_name'])
        print("3: ", "Match null")
        response = input("Résultat: ")
        return response
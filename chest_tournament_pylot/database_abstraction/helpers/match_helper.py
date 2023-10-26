from chest_tournament_pylot.database_abstraction.models.database_helper import pull_database_obj
from chest_tournament_pylot.database_abstraction.models.round import Round
from chest_tournament_pylot.database_abstraction.models.tournament import Tournament

class MatchHelper:
    
    def create_match_lst(self, player_lst, round_lst):

        match_lst = []
        player_lst = sorted(player_lst, key=lambda x: x["score"], reverse=True)

        while len(player_lst) >= 2:

            player_id_1, player_id_2 = self.players_pairing_creation(player_lst, round_lst)

            match = [{"player_id": player_id_1, "result": None}, {"player_id": player_id_2, "result": None}]
            match_lst.append(match)

            player_lst = list(filter(lambda player: player['player_id'] not in [player_id_1, player_id_2], player_lst))
        return match_lst


    def players_pairing_creation(self, player_lst, round_lst):
        index = 1
        player_to_pair_with = self.choose_player(index, player_lst, round_lst)
        if player_to_pair_with == None:
            return player_lst[0]['player_id'], player_lst[1]['player_id']
        else:
            return player_lst[0]['player_id'], player_to_pair_with['player_id']   


    def choose_player(self, index, player_lst, round_lst):
        
        if round_lst is not None:
            if self.check_if_already_played(player_lst[0], player_lst[index], round_lst) is True:
                print("TRUE")
                index += 1
                if index < len(player_lst):
                    return self.choose_player(index, player_lst, round_lst)
            else:
                print(player_lst[0], player_lst[index])
                return player_lst[index]


            
    def check_if_already_played(self, player_1, player_2, round_lst):
        is_already_played = False
        for round in round_lst:
            # print("ROUND LIST", round.number)
            for match in round.match_lst:
                print(match[0]['player_id'], player_1['player_id'], player_2['player_id'], match[1]['player_id'])
                if match[0]['player_id'] == player_1['player_id'] and player_2['player_id']== match[1]['player_id']:                    
                    is_already_played = True
                    print(is_already_played)
                    return is_already_played
        print(is_already_played)
        return is_already_played
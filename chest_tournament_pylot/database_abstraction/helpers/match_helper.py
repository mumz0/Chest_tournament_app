from chest_tournament_pylot.database_abstraction.models.round import Round


class MatchHelper:
    
    def create_match_lst(self, player_lst):
        match_lst = []
        player_lst = sorted(player_lst, key=lambda x: x["score"], reverse=True)

        while len(player_lst) >= 2:
            # print(player_lst)
            player_id_1, player_id_2 = self.players_pairing_creation(player_lst)
            print(player_id_1, player_id_2)
            match = [{"player_id": player_id_1, "result": None}, {"player_id": player_id_2, "result": None}]
            match_lst.append(match)

            player_lst = list(filter(lambda player: player['player_id'] not in [player_id_1, player_id_2], player_lst))
        return match_lst


    def players_pairing_creation(self, player_lst):
        index = 1
        player_to_pair_with = self.choose_player(index, player_lst)
        if player_to_pair_with == None:
            return player_lst[0]['player_id'], player_lst[1]['player_id']
        else:
            return player_lst[0]['player_id'], player_to_pair_with['player_id']   


    def choose_player(self, index, player_lst):
        if player_lst[0]['score'] == player_lst[index]['score']:
            index += 1
            if index < len(player_lst):
                self.choose_player(index, player_lst)
            else:
                return None
        else:
            return player_lst[index]
            
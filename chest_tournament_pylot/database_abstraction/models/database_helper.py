class DatabaseHelper:

    def save(obj, db):
        db.insert(obj)

    def pull_database_obj_lst(db):
        return db.all()

    def pull_database_obj(id, db):
        result = db.get(doc_id=id)
        result.doc_id
        return result

    def pull_database_lst(ids_lst, db):
        objs_lst = []
        for id in ids_lst:
            result = db.get(doc_id=id)
            objs_lst.append(result)
        return objs_lst

    # Fonction pour mettre à jour round_lst
    def update_tournament_round(tournament_id, round_serialized, db):
        table = db.table('_default')
        tournament = table.get(doc_id=int(tournament_id))
        tournament['round_lst'].append(round_serialized)
        table.update({'round_lst': tournament['round_lst']}, doc_ids=[int(tournament.doc_id)])

    # Fonction pour mettre à jour round_lst
    def update_match_and_player_score(tournament_id, round_number, result_match, db):
        table = db.table('_default')
        tournament = table.get(doc_id=int(tournament_id))

        for match in tournament['round_lst'][int(round_number) - 1]['match_lst']:
            if (match[0]["player_id"] == result_match[0]["player_id"] and
                    match[1]["player_id"] == result_match[1]["player_id"]):
                match[0]['result'] = result_match[0]['result']
                match[1]['result'] = result_match[1]['result']
        table.update({'round_lst': tournament['round_lst']}, doc_ids=[int(tournament.doc_id)])

        for player in tournament['players']:
            if player['player_id'] == result_match[0]['player_id']:
                player['score'] += result_match[0]['result']

            if player['player_id'] == result_match[1]['player_id']:
                player['score'] += result_match[1]['result']

        table.update({'players': tournament['players']}, doc_ids=[int(tournament.doc_id)])

    def update_end_date_tournament(end_date, tournament_id, db):
        table = db.table('_default')
        tournament = table.get(doc_id=int(tournament_id))
        tournament["end_date"] = end_date
        table.update(tournament, doc_ids=[int(tournament.doc_id)])

    def update_end_time_round(round_end_timestamp, round_number, tournament_id, db):
        table = db.table('_default')
        tournament = table.get(doc_id=int(tournament_id))
        tournament['round_lst'][int(round_number) - 1]['end_timestamp'] = round_end_timestamp
        db.table('_default').update({'round_lst': tournament['round_lst']}, doc_ids=[int(tournament.doc_id)])

    def pull_tournament_attr(attr, tournament_id, db):
        table = db.table('_default')
        tournament = table.get(doc_id=int(tournament_id))
        return tournament[attr]

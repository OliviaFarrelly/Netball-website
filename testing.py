from db_functions import run_search_query_tuples


def get_game(db_path):
    sql = """ select game.gamedate, game.location, game.team1, game.score1, game.team2, game.score2 
    from game
    """
    result = run_search_query_tuples(sql, (), db_path, True)
    for row in result:
        for k in row.keys():
            print(k)
            print(row[k])


if __name__ == "__main__":
    db_path = 'data/netball_db.sqlite'
    get_game(db_path)

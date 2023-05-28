from db_functions import run_search_query_tuples


def get_notices(db_path):
    sql = """ select notices.title, notices.content, member.name
    from notices
    join member on notices.member_id = member.member_id;
    """
    result = run_search_query_tuples(sql, (), db_path, True)
    for row in result:
        for k in row.keys():
            print(k)
            print(row[k])


if __name__ == "__main__":
    db_path = 'data/netball_db.sqlite'
    get_notices(db_path)

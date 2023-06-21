from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query_tuples, run_commit_query
from datetime import datetime


app = Flask(__name__)
app.secret_key = "sgdjkdgjdfgkdjfgk"
db_path = 'data/netball_db.sqlite'


@app.template_filter()
def noticedate(sqlite_dt):
    # create a data object
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %y %I:%M %p")


@app.template_filter()
def gameday(sqlite_dt):
    # create a data object
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b")


@app.template_filter()
def resultdate(sqlite_dt):
    # create a data object
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d')
    return x.strftime("%a %d %b")


@app.template_filter()
def gametime(sqlite_dt):
    # create a data object
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%I:%M %p")


@app.route('/notices_cud', methods=['GET', 'POST'])
def notices_cud():
    # collect data from the web address
    data = request.args
    required_keys = ['id', 'task']
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with create read update on notice (key not present)"
            return render_template('error.html', message=message)
    # have an id and task key
    if request.method == "GET":
        if data['task'] == 'delete':
            sql = "delete from notices where notices_id = ?"
            values_tuple = (data['id'],)
            run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('index'))
        elif data['task'] == 'update':
            sql = """select title, content from notices where notices_id = ?"""
            values_tuple = (data['id'],)
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("notices_cud.html",
                                   **result,
                                   id=data['id'],
                                   task=data['task'])
        elif data['task'] == 'add':
            temp = {'title': 'Test Title', 'content': 'Test Content'}
            return render_template("notices_cud.html",
                                   id=0,
                                   task=data['task'],
                                   **temp)
        else:
            message = "Unrecognised task coming from notices page"
            return render_template('error.html', message=message)
    elif request.method == "POST":
        # collected form information
        f = request.form
        print(f)
        if data['task'] == 'add':
            # add the new entry to the database
            # member is fixed for now
            sql = """ insert into notices(title, content, noticedate, member_id)
                                values(?,?, datetime('now', 'localtime'),?) """
            values_tuple = (f['title'], f['content'], session['member_id'])
            run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('index'))
        elif data['task'] == 'update':
            sql = """ update notices set title=?, content=?, 
                            noticedate=datetime('now', 'localtime') where notices_id=?"""
            values_tuple = (f['title'], f['content'], data['id'])
            result = run_commit_query(sql, values_tuple, db_path)
            # collect teh data from the form and update the database at the sent id
        return redirect(url_for('index'))

    else:
        return render_template("notices_cud.html")


@app.route('/')
def index():
    # query for the news items for the page
    sql = """ select notices.notices_id , notices.title, notices.content, notices.noticedate, member.name
    from notices
    join member on notices.member_id = member.member_id
    order by notices.noticedate desc;
    """
    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("index.html", notices=result)


@app.route('/login', methods=["GET", "POST"])
def login():
    print(session)
    error = "Your credentials are not recognised"
    if request.method == "GET":
        return render_template("login.html", email='Dave_coach@g.com', password="temp")
    elif request.method == "POST":
        f = request.form
        sql = """ select member_id, name, password, authorisation from member where email = ? """
        values_tuple = (f['email'],)
        result = run_search_query_tuples(sql, values_tuple, db_path, True)
        if result:
            # allowed result
            result = result[0]
            # check result password from query with the form
            if result['password'] == f['password']:
                # start a session
                session['name'] = result['name']
                session['authorisation'] = result['authorisation']
                session['member_id'] = result['member_id']
                print(session)
                # match login is allowed go back to home page
                return redirect(url_for('index'))
            else:
                # if there is a problem take it back to the login page
                return render_template("login.html", email='Dave_coach@g.com', password="temp", error=error)

        else:
            return render_template("login.html", email='Dave_coach@g.com', password="temp", error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/team')
def team():
    return render_template("team.html")


@app.route('/draws')
def draws():
    sql = """ select game.game_id , game.gamedate, game.team1, game.team2
       from game
       order by game.gamedate ASC
       """
    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("draws.html", draws=result)


@app.route('/draws_cud', methods=['GET', 'POST'])
def draws_cud():
    # collect data from the web address
    data = request.args
    required_keys = ['id', 'task']
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with create read update on draws (key not present)"
            return render_template('error.html', message=message)
    if request.method == "GET":
        if data['task'] == 'delete':
            sql = "delete from game where game_id = ?"
            values_tuple = (data['id'],)
            run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('draws'))
        elif data['task'] == 'update':
            sql = "select gamedate, team1, team2 from game where game_id =?"
            values_tuple = (data['id'],)
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("draws_cud.html",
                                   gamedate=result['gamedate'].replace(" ", "T"),
                                   team1=result['team1'],
                                   team2=result['team2'],
                                   id=data['id'],
                                   task=data['task'])
        elif data['task'] == 'add':
            return render_template("draws_cud.html", id=0, task='add')
        else:
            message = "unrecognised task"
            return render_template('error.html', message=message)
    elif request.method == "POST":
        f = request.form
        print(f)
        if data['task'] == 'add':
            sql = """insert into game(gamedate,team1,team2,location)
            values(?,?,?,?)"""
            g_date = f['gamedate'].replace("T", " ")+":00"
            values_tuple = (g_date, f['team1'], f['team2'], "ASB")
            result = run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('draws'))
        elif data['task'] == 'update':
            sql = """ update game set gamedate=?, team1=?, team2=? where game_id = ? """
            g_date = f['gamedate'].replace("T", " ") + ":00"
            values_tuple = (g_date, f['team1'], f['team2'], data['id'])
            result = run_commit_query(sql, values_tuple, db_path)
            # collect teh data from the form and update the database at the sent id
        return redirect(url_for('draws'))
    else:
        return render_template("draws_cud.html")


@app.route('/results')
def results():
    sql = """ select game.game_id , game.gamedate, game.team1, 
                game.score1, game.team2, game.score2
           from game
           order by game.gamedate DESC 
           """
    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("results.html", results=result)


@app.route('/results_cud', methods=['GET', 'POST'])
def results_cud():
    # collect data from the web address
    data = request.args
    required_keys = ['id', 'task']
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with create read update on draws (key not present)"
            return render_template('error.html', message=message)
    if request.method == "GET":
        if data['task'] == 'delete':
            sql = "delete from game where game_id = ?"
            values_tuple = (data['id'],)
            run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('results'))
        elif data['task'] == 'update':
            sql = "select gamedate, team1, score1, team2, score2 from game where game_id =?"
            values_tuple = (data['id'],)
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("results_cud.html",
                                   gamedate=result['gamedate'].replace(" ", "T"),
                                   team1=result['team1'],
                                   score1=result['score1'],
                                   team2=result['team2'],
                                   score2=result['score2'],
                                   id=data['id'],
                                   task=data['task'])

        else:
            message = "unrecognised task"
            return render_template('error.html', message=message)
    elif request.method == "POST":
        f = request.form
        print(f)
        if data['task'] == 'update':
            print("updating")
            sql = """ update game set gamedate=?, team1=?, score1=?, team2=?, score2=? where game_id=?"""
            g_date = f['gamedate'].replace("T", " ") + ":00"
            values_tuple = (g_date, f['team1'], f['score1'], f['team2'], f['score2'], data['id'])
            result = run_commit_query(sql, values_tuple, db_path)
            print(result)
            # collect teh data from the form and update the database at the sent id
        return redirect(url_for('results'))
    else:
        return render_template("results_cud.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        f = request.form
        print(f)
        return render_template("confirm.html", form_data=f)
    elif request.method == "GET":
        temp_form_data = {
            "firstname": "Olivia",
            "lastname": "Farrelly",
            "age": "17",
            "youremail": "olivia.farrelly@marsden.school.nz",
            "emergencyemail": "nzsamiam@gmail.com",
            "aboutme": "I have played netball for 3 years and im a GA and GS"
        }
        return render_template("register.html", **temp_form_data)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)

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
    return redirect (url_for('index'))



@app.route('/team')
def team():
    return render_template("team.html")


@app.route('/draws')
def draws():
    return render_template("draws.html")


@app.route('/results')
def results():
    return render_template("results.html")


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
    app.run(debug=True)

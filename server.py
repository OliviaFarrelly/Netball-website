from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


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
            "firstname": "Daisy",
            "lastname": "Prune",
            "age": "13",
            "youremail": "daisyprune@email.com",
            "parentsemail": "ellaprune@gmail.com",
            "aboutme": "I have played netball for 3 years and im a GA and GS"
        }
        return render_template("register.html", **temp_form_data)


if __name__ == "__main__":
    app.run(debug=True)

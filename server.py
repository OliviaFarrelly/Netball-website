from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1> Hello World </h1>"


@app.route('/team')
def team():
    return "<h1>Team Page </h1>"


@app.route('/draws_results')
def draws_results():
    return "<h1>Draws & Results</h1>"


@app.route('/register')
def register():
    return "<h1>Register</h1>"


if __name__ == "__main__":
    app.run(debug=True)

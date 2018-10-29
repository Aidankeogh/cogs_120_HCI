from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import yaml


# Check out flask cheat sheet here
# https://s3.us-east-2.amazonaws.com/prettyprinted/flask_cheatsheet.pdf

app = Flask(__name__)
Bootstrap(app)

with open('backend.yaml', 'r') as f:
    backend = yaml.load(f)

@app.route('/')
def home():
    return render_template('home.html', backend = backend)

@app.route('/login')
def login():
    return render_template('login.html', backend = backend)

@app.route('/about')
def about():
    return render_template('about.html', backend = backend)

@app.route('/xyz')
def event():
    return render_template('event.html', backend = backend, event = backend['events']['xyz'])

@app.route('/xyz/edit')
def edit_event():
    return render_template('home.html', backend = backend, event = backend['events']['xyz'])

@app.route('/<username>')
def user(username):
    return render_template('profile.html', backend = backend, event = backend['users']['jane_doe'])


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

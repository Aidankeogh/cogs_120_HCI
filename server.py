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

@app.route('/login', methods=['GET', 'POST'])
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
    return render_template('event.html', backend = backend, event = backend['events']['xyz'])

@app.route('/new_event')
def create_event():
    return render_template('new_event.html', backend = backend)

@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html', backend = backend)

@app.route('/jane_doe')
def other_profile():
    return render_template('other_profile.html', backend = backend)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

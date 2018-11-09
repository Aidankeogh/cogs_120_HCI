from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from backend import backend, get_tiles
import yaml

# Check out flask cheat sheet here
# https://s3.us-east-2.amazonaws.com/prettyprinted/flask_cheatsheet.pdf

app = Flask(__name__)
Bootstrap(app)



@app.route('/')
def home():
    return render_template('search.html', backend = backend, user=backend['user'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', backend = backend)

@app.route('/about')
def about():
    return render_template('about.html', backend = backend)

@app.route('/search')
def search():
    return render_template('search.html', backend = backend)

@app.route('/new_event')
def new_event():
    return render_template('new_event.html', backend = backend)

@app.route('/<something>')
def other_profile(something):
    if something in backend['users']:
        user = something
        return render_template('profile.html', backend = backend, user=user)
    elif something in backend['events'] :
        event = something
        return render_template('event.html', backend = backend, event=backend['events'][event])
    else:
        return render_template('404')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

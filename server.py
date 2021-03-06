from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from backend import get_backend, set_backend
from search import search_events
import yaml
import string
import random
# Check out flask cheat sheet here
# https://s3.us-east-2.amazonaws.com/prettyprinted/flask_cheatsheet.pdf

app = Flask(__name__)
Bootstrap(app)

def create_url():
    url = ''
    for i in range(3):
        url += random.choice(string.ascii_letters + string.digits)
    return url

backend = get_backend()
@app.route('/', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def search():
    backend = get_backend()
    eventlist = backend['events'].keys()
    eventlist.sort()
    query = request.args.get('query')
    if query:
        eventlist = search_events(query,backend)
    if request.args.get('f_friend') == 'True':
        for e in backend['events'].keys():
            if e in eventlist and backend['events'][e]['friends'] == 0:
                eventlist.remove(e)
    if request.args.get('f_faculty') == 'True':
        for e in backend['events'].keys():
            if e in eventlist and backend['events'][e]['badge_counts'][0] == 0:
                eventlist.remove(e)
    if request.args.get('f_research') == 'True':
        for e in backend['events'].keys():
            if e in eventlist and backend['events'][e]['badge_counts'][1] == 0:
                eventlist.remove(e)
    if request.args.get('f_clubs') == 'True':
            for e in backend['events'].keys():
                if e in eventlist and backend['events'][e]['badge_counts'][2] == 0:
                    eventlist.remove(e)
    if request.args.get('f_industry') == 'True':
        for e in backend['events'].keys():
            if e in eventlist and backend['events'][e]['badge_counts'][3] == 0:
                eventlist.remove(e)




    if request.method == 'POST': #this block is only entered when the form is submitted
        r = request.form
        print r
        if  'edit' in r: # attend event
            link = r['edit']
            e = backend['events'][link]
            e['title'] = r[link+'title']
            e['date'] = r[link+'date']
            e['location'] = r[link+'location']
            e['description'] = r[link+'description']
        if  'attend' in r: # attend event
            link = r['attend']
            e = backend['events'][link]
            if backend['logged_in']:
                e['attendees'].append(r[link+'name'])
                backend['users'][backend['user']]['events'].append(link)
            elif " + " + r[link+'name'] not in e['attendees']:
                e['attendees'].append(" + " + r[link+'name'])
        if  'unattend' in r: # attend event
            link = r['unattend']
            e = backend['events'][link]
            e['attendees'].remove(r[link+'name'])
            backend['users'][backend['user']]['events'].remove(link)
        set_backend(backend)

    return render_template('search.html', backend = backend, eventlist = eventlist)

@app.route('/<something>', methods=['GET', 'POST'])
def other_profile(something):
    backend = get_backend()
    if request.method == 'POST': #this block is only entered when the form is submitted
        r = request.form
        print r
        if  'edit' in r: # attend event
            link = r['edit']
            e = backend['events'][link]
            e['title'] = r[link+'title']
            e['date'] = r[link+'date']
            e['location'] = r[link+'location']
            e['description'] = r[link+'description']
        if  'attend' in r: # attend event
            link = r['attend']
            e = backend['events'][link]
            if backend['logged_in']:
                e['attendees'].append(r[link+'name'])
                backend['users'][backend['user']]['events'].append(link)
            elif " + " + r[link+'name'] not in e['attendees']:
                e['attendees'].append(" + " + r[link+'name'])

        if  'unattend' in r: # attend event
            link = r['unattend']
            e = backend['events'][link]
            e['attendees'].remove(r[link+'name'])
            backend['users'][backend['user']]['events'].remove(link)
        if 'edituser' in r:
            link = r['edituser']
            u = backend['users'][link]
            u['name'] = r[link+'name']
            u['picture'] = r[link+'picture']
            u['about'] = r[link+'about']
            u['email'] = r[link+'email']
            if r[link+'Faculty'] == '' or r[link+'Faculty'] == 'None':
                u['badges'][0] = None
            else:
                u['badges'][0] = r[link+'Faculty']
            if r[link+'Research'] == '' or r[link+'Research'] == 'None':
                u['badges'][1] = None
            else:
                u['badges'][1] = r[link+'Research']
            if r[link+'Clubs'] == '' or r[link+'Clubs'] == 'None':
                u['badges'][2] = None
            else:
                u['badges'][2] = r[link+'Clubs']
            if r[link+'Industry'] == '' or r[link+'Industry'] == 'None':
                u['badges'][3] = None
            else:
                u['badges'][3] = r[link+'Industry']
        if 'newevent' in r:
            url = create_url()
            while(url in backend['events']):
                url = create_url()
            backend['events'][url] = {}
            e = backend['events'][url]
            e['attendees'] = []
            e['host'] = backend['user']
            e['title'] = r['newtitle']
            e['date'] = r['newdate']
            e['description'] = r['newdescription']
            e['location'] = r['newlocation']
            e['img_src'] = ''
            e['link'] = url
            backend['users'][backend['user']]['events'].append(url)
            set_backend(backend)
            return redirect("/"+url, code=302)
        if 'delete' in r:
            link = r['delete']
            e = backend['events'][link]
            for user in e['attendees']:
                backend['users'][user]['events'].remove(link)
            backend['users'][e['host']]['events'].remove(link)
            del backend['events'][link]
            set_backend(backend)
            return redirect("/", code=302)
        if 'addfriend' in r:
            link = r['addfriend']
            u = backend['users'][link]
            u['friends'].append(r[link+'friend'])
            print u['friends']
        if 'unfriend' in r:
            link = r['unfriend']
            u = backend['users'][link]
            u['friends'].remove(r[link+'unfriend'])
            print u['friends']
        set_backend(backend)

    if something in backend['users']:
        user = something
        return render_template('profile.html', backend = backend, user=user)
    elif something in backend['events'] :
        event = something
        return render_template('event.html', backend = backend, event=backend['events'][event])
    else:
        return '404'

@app.route('/login', methods=['GET', 'POST'])
def login():
    backend = get_backend()
    if backend['logged_in'] :
        print 'here'
        backend['user'] = None
        backend['logged_in'] = False
        print backend
        set_backend(backend)

    if request.method == 'POST': #this block is only entered when the form is submitted
        r = request.form
        if 'login' in r:
            backend['logged_in'] = True
            if request.form['username'] not in backend['users']:
                backend['user'] = 'percy'
            else:
                backend['user'] = request.form['username']
            set_backend(backend)
            return redirect("/"+backend['user'], code=302)
        if 'create' in r:
            backend['users'][r['link']] = {}
            u = backend['users'][r['link']]
            u['name'] = r['name']
            u['link'] = r['link']
            u['badges'] = [None,None,None,None]
            u['events'] = []
            u['email'] = r['email']
            u['about'] = ''
            u['friends'] = []
            if r['picture'] != '':
                u['picture'] = r['picture']
            else:
                u['picture'] = "https://bootdey.com/img/Content/avatar/avatar"+ str(random.choice([1,2,3,4,5,6,7,8])) + ".png"
            backend['user'] = r['link']
            backend['logged_in'] = True
            set_backend(backend)
            return redirect("/"+backend['user'], code=302)


    return render_template('login.html', backend = backend)

@app.route('/favicon.ico')
def favicon():
    return 'null'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

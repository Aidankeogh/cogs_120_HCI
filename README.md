# cogs_120_hci


Requires a working install of python 2, with pip. 

LINUX/MAC:
To install requirements: 

pip install -r requirements.txt

To launch server:

python server.py

WINDOWS: 
Requirements:

Windows command prompt:
CD to the folder you want (cd C:/bla/bla/bla/bla/cogs_120_hci) 
‘py -m pip install -r requirements.txt’

Server:

Windows command prompt:
CD to the folder you want (cd C:/bla/bla/bla/bla/cogs_120_hci) 
‘py server.py’

This should set up the website on 0.0.0.0:5000, type that into a browser and you can view the site. 
--------------------------------------------------------------------------------------------------------------------------------
Tinkering with stuff:
Inside of server.py you can see how the pages are set up. 

Each line like:

@app.route('/about')
def about():
    return render_template('about.html', backend = backend)

Makes it so 0.0.0.0:5000/about renders the ‘about.html’ page. You can start tinkering with the about.html page in /cogs_120_hci/templates/about.html

At the top of about.html is “ extends ‘base.html “. Basically base.html is just where stuff that goes on every page like the navbar is placed. Anything that is specific to the about page should be between 
{% block content %}
And 
{% endblock %}
So you don’t need to worry about re-writing html that is on every page. 

If you’re curious about these blocks, they’re from jinja2 templating, which is something that comes with flask. How they work is that it renders base.html, but with base.html’s content block replaced with the content block written in about.html


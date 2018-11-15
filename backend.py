from jinja2 import Template
import yaml

def get_tiles(backend):
    badges = backend['badges']
    for event in backend['events']:
        event = backend['events'][event]
        event['hosting'] = (event['host'] == backend['user'])
        badge_counts = [0] * len(badges)
        attendees = 0
        friends = 0

        for attendee in event['attendees'] + [event['host']]:
            attendees += 1    
            if attendee in backend['users']:
                if backend['logged_in'] and attendee in backend['users'][backend['user']]['friends']:
                    friends += 1
                for i in range(len(badges)):
                    if backend['users'][attendee]['badges'][i]:
                        badge_counts[i] += 1

        event['friends'] = friends
        event['num_attendees'] = attendees
        event['badge_counts'] = badge_counts

def get_backend():
    with open('backend.yaml', 'r') as f:
        backend = yaml.load(f)

    with open('templates/event_tile.html') as file:
        event_template = Template(file.read())
    with open('templates/user_tile.html') as file:
        user_template = Template(file.read())

    get_tiles(backend)
    return backend

def set_backend(b):
    with open('backend.yaml', 'w') as f:
        yaml.dump(b, f, default_flow_style=False)

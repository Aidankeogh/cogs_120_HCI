from jinja2 import Template
import yaml

with open('backend.yaml', 'r') as f:
    backend = yaml.load(f)

with open('templates/event_tile.html') as file:
    event_template = Template(file.read())
with open('templates/user_tile.html') as file:
    user_template = Template(file.read())


badges = backend['badges']

def get_tiles():
    for event in backend['events']:
        event = backend['events'][event]
        event['hosting'] = (event['host'] == backend['user'])
        badge_counts = [0] * len(badges)
        attendees = 0
        friends = 0

        for attendee in event['attendees'] + [event['host']]:
            attendees += 1
            if backend['logged_in'] and attendee in backend['users'][backend['user']]['friends']:
                friends += 1
            for i in range(len(badges)):
                if backend['users'][attendee]['badges'][i]:
                    badge_counts[i] += 1

        event['friends'] = friends
        event['num_attendees'] = attendees
        event['badge_counts'] = badge_counts

get_tiles()

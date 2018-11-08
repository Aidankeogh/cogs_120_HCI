from jinja2 import Template
import yaml

with open('backend.yaml', 'r') as f:
    backend = yaml.load(f)

with open('templates/event_tile.html') as file:
    event_template = Template(file.read())
with open('templates/user_tile.html') as file:
    user_template = Template(file.read())


badges = backend['badges']

def get_tiles(user):
    for event in backend['events']:
        event = backend['events'][event]
        event['hosting'] = (event['host'] == user)
        badge_counts = [0] * len(badges)
        attendees = 0
        friends = 0

        for attendee in event['attendees'] + [event['host']]:
            attendees += 1
            if attendee in backend['users'][backend['user']]['friends']:
                friends += 1
            for i in range(len(badges)):
                if backend['users'][attendee]['badges'][i]:
                    badge_counts[i] += 1

        event['event_tile'] = event_template.render(current_user=user,
                                                    event=event,
                                                    host=backend['users'][event['host']],
                                                    attendees=attendees,
                                                    friends=friends,
                                                    badges=badges,
                                                    badge_counts=badge_counts)

for user, user_profile in backend['users'].iteritems():
    user_profile['user_tile'] = user_template.render(user=user_profile, badges=badges)
    get_tiles(user)

get_tiles(backend['user'])

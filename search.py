import string
def textify(event,backend):
    text = event['host']
    for attendee in event['attendees'] + [event['host']]:
        if attendee in backend['users']:
            text += ' ' + backend['users'][attendee]['name']
            for badge in backend['users'][attendee]['badges']:
                if badge:
                    text += ' ' + badge
    text += ' ' + event['title']
    text += ' ' + event['description']
    text += ' ' + event['location']
    return str(text).lower().translate(None,string.punctuation).split()

def search_events(query, backend):
    query = str(query).lower().split()
    results = []
    for link, event in backend['events'].items():
        event_text = textify(event,backend)
        score = 0
        for word in query:
            score += event_text.count(word)
        if score > 0:
            results.append((link,score))
    results.sort(key = lambda t: t[1])
    results.reverse()
    return [r[0] for r in results]

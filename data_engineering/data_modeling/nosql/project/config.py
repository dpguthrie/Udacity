sparkify_dictionary = {
    'item': {
        'table': 'item_detail',
        'columns': ['sessionId', 'itemInSession', 'artist', 'song', 'length'],
        'column_types': ['int', 'int', 'text', 'text', 'float'],
        'primary_key': ['sessionId', 'itemInSession'],
        'select': {
            'columns': ['artist', 'song', 'length'],
            'where': ["sessionId = 338", "itemInSession = 4"],
            'description': 'This query aims to get the detail of a song for \
                one specific item in a session'
        }
    },
    'session': {
        'table': 'session_detail',
        'columns': ['sessionId', 'itemInSession', 'artist', 'song', 'userId',
                    'firstName', 'lastName'],
        'column_types': ['int', 'int', 'text', 'text', 'int', 'text', 'text'],
        'primary_key': [('userId', 'sessionId'), 'itemInSession'],
        'select': {
            'columns': ['artist', 'song', 'firstname', 'lastname'],
            'where': ["userId = 10", "sessionId = 182"],
            'description': 'This query aims to find all songs a user listened \
                to in a particular session'
        }
    },
    'song': {
        'table': 'song_detail',
        'columns': [
            'song', 'userId', 'firstName', 'lastName'],
        'column_types': ['text', 'int', 'text', 'text'],
        'primary_key': ['song', 'userId'],
        'select': {
            'columns': ['firstname', 'lastname'],
            'where': ["song = 'All Hands Against His Own'"],
            'description': 'This query aims to find all users who have \
                listened to a specific song'
        }
    }
}

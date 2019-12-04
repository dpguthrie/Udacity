sparkify_dictionary = {
    'item': {
        'table': 'item_detail',
        'columns': ['sessionId', 'itemInSession', 'artist', 'song', 'length'],
        'column_types': ['int', 'int', 'text', 'text', 'float'],
        'primary_key': ['sessionId', 'itemInSession']
    },
    'session': {
        'table': 'session_detail',
        'columns': ['sessionId', 'itemInSession', 'artist', 'song', 'userId',
                    'firstName', 'lastName'],
        'column_types': ['int', 'int', 'text', 'text', 'int', 'text', 'text'],
        'primary_key': ['userId', 'sessionId', 'itemInSession']
    },
    'song': {
        'table': 'song_detail',
        'columns': [
            'sessionId', 'itemInSession', 'song', 'firstName', 'lastName'],
        'column_types': ['int', 'int', 'text', 'text', 'text'],
        'primary_key': ['song', 'sessionId', 'itemInSession']
    }
}

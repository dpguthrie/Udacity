sparkify_dictionary = {
    'item': {
        'table': 'item_detail',
        'columns': ['sessionId', 'itemInSession', 'artist', 'song', 'length'],
        'column_types': ['int', 'int', 'text', 'text', 'float'],
        'primary_key': ['sessionId', 'itemInSession'],
        'primary_key_description': '''
            The item_detail table uses a compound primary key with two components:
            sessionId and itemInSession.  The sessionId will be how the data
            is partitioned in the cluster and itemInSession will (1)
            enforce uniqueness on the row and (2) order the data in ascending
            order.  The query used for this table is concerned with a specific
            item in a session so it made sense to me to partition the data by
            session.
        '''
    },
    'session': {
        'table': 'session_detail',
        'columns': ['sessionId', 'itemInSession', 'artist', 'song', 'userId',
                    'firstName', 'lastName'],
        'column_types': ['int', 'int', 'text', 'text', 'int', 'text', 'text'],
        'primary_key': ['userId', 'sessionId', 'itemInSession'],
        'primary_key_description': '''
            The session_detail table uses a compound primary key with three
            components:  userId, sessionId, and itemInSession.  The userId will
            be how the data is partitioned in the cluster and sessionId and
            itemInSession will (1) enforce uniqueness on the row and (2) order
            the data in ascending order.  The query used for this table is
            concerned with a specific user and session so it made sense to me
            to partition the data by user.
        '''
    },
    'song': {
        'table': 'song_detail',
        'columns': [
            'sessionId', 'itemInSession', 'song', 'firstName', 'lastName'],
        'column_types': ['int', 'int', 'text', 'text', 'text'],
        'primary_key': ['song', 'sessionId', 'itemInSession'],
        'primary_key_description': '''
            The song_detail table uses a compound primary key with three
            components:  song, sessionId, and itemInSession.  The song will
            be how the data is partitioned in the cluster and sessionId and
            itemInSession will (1) enforce uniqueness on the row and (2) order
            the data in ascending order.  The query used for this table is
            concerned with a specific song so it made sense to me
            to partition the data by song.
        '''
    }
}

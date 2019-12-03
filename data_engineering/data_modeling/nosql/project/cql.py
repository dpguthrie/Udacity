from cassandra.cluster import Cluster

from .utils import convert_list_to_string


class Connection:
    def __init__(self, host, keyspace, **kwargs):
        self.host = host
        self.keyspace = keyspace
        self.cluster = self._cluster
        self.session = self.cluster.connect()
        self.session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {keyspace}
            WITH REPLICATION = {
                'class': 'SimpleStrategy',
                'replication_factor': 1
            }
        """)
        self.session.set_keyspace(self.keyspace)

    @property
    def _cluster(self):
        try:
            cluster = Cluster([self.host])
            return cluster
        except Exception as e:
            print(e)


class Cassandra(Connection):
    def __init__(self, dictionary, dataframe, host='127.0.0.1'):
        super().__init__(host)
        self.dictionary = dictionary
        self.dataframe = dataframe

    def _table(self, key):
        return self.dictionary[key]['table']

    def _columns(self, key):
        """List of columns as specified in dictionary

        Arguments:
            key {str} -- Represents key in self.dictionary

        Returns:
            list -- List of columns
        """
        return self.dictionary[key]['columns']

    def _column_types(self, key):
        """List of column types as specified in dictionary

        Arguments:
            key {str} -- Represents key in self.dictionary

        Returns:
            list -- List of column types
        """
        return self.dictionary[key]['column_types']

    def _columns_with_types(self, key):
        columns = self._columns(key)
        column_types = self._column_types(key)
        return ', '.join(' '.join(x) for x in zip(columns, column_types))

    def _column_placeholders(self, key):
        columns = self._columns(key)
        placeholders = '%s, ' * len(columns)
        return placeholders[:-2]

    def _primary_key(self, key):
        return self.dictionary[key]['primary_key']

    def create_statement(self, key):
        return f'''
            CREATE TABLE IF NOT EXISTS {self._table}
            ({convert_list_to_string(self._columns_with_types)},
            PRIMARY KEY ({convert_list_to_string(self._primary_key)}))
        '''

    def insert_statement(self, key):
        return f'''
            INSERT INTO {self._table} ({convert_list_to_string(self._columns)})
            VALUES ({self._column_placeholders})
        '''

    def _execute(self, query, params=()):
        try:
            self.session.execute(query, params=params)
        except Exception as e:
            print(e)

    def run(self, key):
        self._execute(self.create_statement(key))
        for i, row in self.dataframe:
            params = [row[column] for column in self._columns]
            self._execute(self.insert_statement(key), params)

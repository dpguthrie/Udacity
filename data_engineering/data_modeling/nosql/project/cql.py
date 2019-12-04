from cassandra.cluster import Cluster

from utils import convert_list_to_string


class Cassandra:
    def __init__(self, host, keyspace, **kwargs):
        self.host = host
        self.keyspace = keyspace
        self.cluster = self._cluster
        self.session = self.cluster.connect()
        self.session.execute("""
            CREATE KEYSPACE IF NOT EXISTS {}
            WITH REPLICATION = {{
                'class': 'SimpleStrategy',
                'replication_factor': 1
            }}
        """.format(self.keyspace))
        self.session.set_keyspace(self.keyspace)

    @property
    def _cluster(self):
        try:
            cluster = Cluster([self.host])
            return cluster
        except Exception as e:
            print(e)


class ETL(Cassandra):
    def __init__(
            self, dictionary, dataframe, host='127.0.0.1', keyspace='udacity'):
        super().__init__(host, keyspace)
        self.dictionary = dictionary
        self.dataframe = dataframe

    def _table(self, key):
        return self.dictionary[key]['table']

    def _columns(self, key):
        """List of columns as specified in self.dictionary

        Arguments:
            key {str} -- Represents key in self.dictionary

        Returns:
            list -- List of columns
        """
        return self.dictionary[key]['columns']

    def _column_types(self, key):
        """List of column types as specified in self.dictionary

        Arguments:
            key {str} -- Represents key in self.dictionary

        Returns:
            list -- List of column types
        """
        return self.dictionary[key]['column_types']

    def _columns_with_types(self, key):
        """Concatenates columns with their respective column types

        Cassandra's CREATE TABLE statement requires the user to specify both
        the column and the column type.

        Arguments:
            key {str} -- Represents key in self.dictionary

        Returns:
            str -- Concatenated string of columns and column types
        """
        columns = self._columns(key)
        column_types = self._column_types(key)
        return ', '.join(' '.join(x) for x in zip(columns, column_types))

    def _column_placeholders(self, key):
        """Number of placeholders to be used in self.insert_statement

        The number of placeholders is determined from the length of
        self._columns

        Arguments:
            key {str} -- Represents key in self.dictionary

        Returns:
            str -- String representing number of placeholders
        """
        columns = self._columns(key)
        placeholders = '%s, ' * len(columns)
        return placeholders[:-2]

    def _primary_key(self, key):
        """Primary Key utilized in self.create_table property

        Arguments:
            key {str} -- Represents key in self.dictionary

        Returns:
            str -- Primary Key
        """
        return self.dictionary[key]['primary_key']

    def create_statement(self, key):
        return f'''
            CREATE TABLE IF NOT EXISTS {self._table(key)}
            ({self._columns_with_types(key)},
            PRIMARY KEY (
                {convert_list_to_string(self._primary_key(key), ", ")}))
        '''

    def insert_statement(self, key):
        return f'''
            INSERT INTO {self._table(key)}
            ({convert_list_to_string(self._columns(key), ", ")})
            VALUES ({self._column_placeholders(key)})
        '''

    def execute(self, query, params=()):
        try:
            self.session.execute(query, params)
        except Exception as e:
            print(e)

    def run(self, key):
        self.execute(self.create_statement(key))
        for i, row in self.dataframe.iterrows():
            params = [row[column] for column in self._columns(key)]
            self.execute(self.insert_statement(key), params)

from common.log import getLogging
logger = getLogging()

class Connection:
    def __init__(self, database):
        if not database:
            raise ValueError("Database must be defined.")

        self.database = database
        from cassandra.cluster import Cluster
        from cassandra.auth import PlainTextAuthProvider
        authProvider = PlainTextAuthProvider(username='cassandra', password='cassandra')
        self.cluster = Cluster(['cassandra'],port=9042, auth_provider=authProvider)
        self.session = self.cluster.connect()
        self.execute(f'USE {self.database}')

    def execute(self, sql, values=None):
        if not values:
            return self.session.execute(sql)
        else:
            prepared = self.session.prepare(sql)
            bound = prepared.bind(values)
            return self.session.execute(bound)

    def query(self, sql, values=None):
        return list(self.execute(sql, values))

    def close(self):
        self.cluster.shutdown()

    def open(self):
        self.session = self.cluster.connect()
        self.execute(f'USE {self.database}')


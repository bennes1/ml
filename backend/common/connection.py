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

    def execute(self, sql):
        self.session.execute(sql)

    def query(self, sql):
        rows = self.session.execute(sql)
        return list(rows)

    def close(self):
        self.cluster.shutdown()


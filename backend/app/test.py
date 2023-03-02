def sample():
    from cassandra.cluster import Cluster
    from cassandra.auth import PlainTextAuthProvider
    authProvider = PlainTextAuthProvider(username='cassandra', password='cassandra')
    cluster = Cluster(['cassandra'],port=9042, auth_provider=authProvider)
    session = cluster.connect('store',wait_for_all_pools=True)
    session.execute('USE store')
    rows = session.execute('SELECT userid, item_count FROM shopping_cart')
    return list(rows)

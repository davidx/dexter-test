def create_cassandra_session():
    username = os.environ.get('CASSANDRA_USERNAME', 'cassandra')
    password = os.environ.get('CASSANDRA_PASSWORD', 'cassandra')
    host = os.environ.get('CASSANDRA_HOST', '127.0.0.1')
    keyspace = os.environ.get('CASSANDRA_KEYSPACE', 'test')
    
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([host], auth_provider=auth_provider)
    session = cluster.connect()
    session.set_keyspace(keyspace)
    return session
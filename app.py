        # Create ScyllaDB connection
        import os
        
        scylladb_username = os.environ.get('SCYLLADB_USERNAME')
        scylladb_password = os.environ.get('SCYLLADB_PASSWORD')
        scylladb_host = os.environ.get('SCYLLADB_HOST')
        scylladb_keyspace = os.environ.get('SCYLLADB_KEYSPACE')
        
        auth_provider = PlainTextAuthProvider(
            username=scylladb_username, password=scylladb_password)
        cluster = Cluster([scylladb_host], auth_provider=auth_provider)
        session = cluster.connect(scylladb_keyspace)
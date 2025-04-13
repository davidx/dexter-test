class TestHealthCheckEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        
    def test_health_check_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'status': 'Healthy'})


class TestDatabaseOperationEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        
    def test_database_operation(self):
        response = self.app.get('/database_operation')
        self.assertEqual(response.status_code, 200)
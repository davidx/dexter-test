class TestDataEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_data_endpoint(self):
        response = self.app.get('/data')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data, [1, 2, 3, 4, 5])


def test_invalid_endpoint(self):
    response = self.app.get('/invalid')
    self.assertEqual(response.status_code, 404)


self.assertEqual(response.headers['Content-Type'], 'application/json')

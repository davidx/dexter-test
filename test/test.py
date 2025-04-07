class TestDataEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_data_endpoint(self):
        DATA_ENDPOINT = '/data'

    def test_data_endpoint(self):
        response = self.app.get(self.DATA_ENDPOINT)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.get_json(), [1, 2, 3, 4, 5])


def test_invalid_endpoint(self):
    response = self.app.get('/invalid')
    self.assertEqual(response.status_code, 404)


# Auto-fix for issue FIX_001:
def test_data_endpoint(self):
    DATA_ENDPOINT = '/data'
    response = self.app.get(DATA_ENDPOINT)
    self.assertEqual(response.status_code, 200)
    self.assertListEqual(response.get_json(), [1, 2, 3, 4, 5])
    # Add additional assertions to verify the response data as needed
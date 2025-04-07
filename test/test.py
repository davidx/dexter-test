class TestDataEndpoint(unittest.TestCase):
    DATA_ENDPOINT = '/data'

    def setUp(self):
        self.app = app.test_client()

    def test_data_endpoint_constant(self):
        DATA_ENDPOINT = '/data'

    def test_data_endpoint_response(self):
        response = self.app.get(self.DATA_ENDPOINT)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.get_json(), [1, 2, 3, 4, 5])


def test_invalid_endpoint():
    app = TestDataEndpoint()
    response = app.app.get('/invalid')
    app.assertEqual(response.status_code, 404)
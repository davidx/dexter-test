class TestDataEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_data_endpoint(self):
        DATA_ENDPOINT = '/data'

    def test_data_endpoint(self):
        response = self.app.get(DATA_ENDPOINT)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.get_json(), [1, 2, 3, 4, 5])


def test_invalid_endpoint(self):
    response = self.app.get('/invalid')
    self.assertEqual(response.status_code, 404)


/* @ DEXTER_AGENT: ISSUE_ID = DUPLICATE_TEST_METHOD * /
/* This code requires improvement: The test class TestDataEndpoint contains two identical test methods named test_data_endpoint. Having duplicate test methods can lead to confusion and maintenance issues. The duplicate method should be removed. */
/* Follow-up agent should implement the necessary changes * /


class TestDataEndpoint(unittest.TestCase):
    DATA_ENDPOINT = '/data'
    INVALID_ENDPOINT = '/invalid'

    def setUp(self):
        self.app = app.test_client()

    def test_data_endpoint(self):
        response = self.app.get(self.DATA_ENDPOINT)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.get_json(), [1, 2, 3, 4, 5])

    def test_invalid_endpoint(self):
        response = self.app.get(self.INVALID_ENDPOINT)
        self.assertEqual(response.status_code, 404)

import unittest
import app
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/health')
def health_check():
    from flask import Flask, jsonify

    return jsonify({
        'status': 'healthy',
        'message': 'Service is up and running'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)


// TODO: Improvement needed - Redundant import statement
// The 'Flask' and 'jsonify' modules are imported twice. This is unnecessary and can lead to confusion.


@app.route('/data')
def data():
    return jsonify([1, 2, 3, 4, 5])


class TestDataEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_data_endpoint(self):
        response = self.app.get('/data')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [1, 2, 3, 4, 5])


if __name__ == '__main__':
    unittest.main()

try:
    # database operation
except Exception as e:
    app.logger.error(f'Error occurred: {e}')
    return jsonify({'error': 'An error occurred'}), 500


@app.route('/search')
def search():
    from elasticsearch import Elasticsearch
    es = Elasticsearch()
    query = request.args.get('q')
    result = es.search(
        index='my-index', body={'query': {'match': {'_all': query}}})
    return jsonify(result)

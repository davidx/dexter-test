from http import HTTPStatus
from flask import Flask, request, jsonify
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
import logging
import sqlite3
import unittest
import os

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Assuming a simple health check is to return a status message
        status = {"status": "Healthy"}
        return jsonify(status), 200
    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Health Check Error: {str(e)}")
        error = {"status": "Unhealthy", "error": str(e)}
        return jsonify(error), 500


@app.route('/')
def home():
    return "Hello, World!"


@app.route('/data')
def data():
    return jsonify([1, 2, 3, 4, 5])


class TestDataEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_data_endpoint(self):
        response = self.app.get('/data')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [1, 2, 3, 4, 5])


def main():
    try:
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        logging.error(
            f"Failed to start Flask app due to {str(e)}", exc_info=True)


if __name__ == '__main__':
    unittest.main()
    main()


@app.route('/database_operation', methods=['GET'])
def database_operation():
    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM example_table')
        result = cursor.fetchall()
        conn.close()

        if result:
            return jsonify(result), 200
        else:
            return jsonify({'message': 'No data found'}), 404
    except sqlite3.Error as e:
        app.logger.error(f'Database error occurred: {str(e)}')
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500
    except Exception as e:
        app.logger.error(f'An unexpected error occurred: {str(e)}')
        return jsonify({'error': 'An internal server error occurred', 'details': str(e)}), 500


def test_health_check_endpoint(self):
    response = self.app.get('/health')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.get_json(), {
                     'status': 'healthy', 'message': 'Service is up and running'})


def test_database_operation(self):
    response = self.app.get('/database_operation')
    self.assertEqual(response.status_code, 200)
    # Add more assertions based on the expected behavior of the function


def create_cassandra_connection():
    # Get database credentials from environment
    scylladb_username = os.environ.get('SCYLLADB_USERNAME', 'cassandra')
    scylladb_password = os.environ.get('SCYLLADB_PASSWORD', 'cassandra')
    scylladb_host = os.environ.get('SCYLLADB_HOST', '127.0.0.1')
    scylladb_keyspace = os.environ.get('SCYLLADB_KEYSPACE', 'test')
    
    # Connect to database
    auth_provider = PlainTextAuthProvider(username=scylladb_username, password=scylladb_password)
    cluster = Cluster([scylladb_host], auth_provider=auth_provider)
    session = cluster.connect(scylladb_keyspace)
    return session


@app.route('/add_user', methods=['POST'])
def add_user():
    # Get user data from request
    user_data = request.get_json()
    
    # Check if data was provided
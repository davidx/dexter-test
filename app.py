from http import HTTPStatus
from flask import Flask, request, jsonify
import logging
import sqlite3
import unittest
import app

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Assuming a simple health check is to return a status message
        return create_response({"status": "Healthy"})
    except Exception as e:
        return error_response(f"Health Check Error: {str(e)}")


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

    def test_health_check_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
                         'status': 'healthy', 'message': 'Service is up and running'})

    def test_database_operation(self):
        response = self.app.get('/database_operation')
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected behavior of the function


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


def create_cassandra_session():
    auth_provider = PlainTextAuthProvider(
        username='cassandra', password='cassandra')
    cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
    session = cluster.connect()
    session.set_keyspace('test')
    return session


@app.route('/add_user', methods=['POST'])
def add_user():
    # Get user data from request
    user_data = request.get_json()
    
    # Check if data was provided
    if not user_data:
        return jsonify({'error': 'No input data provided'}), HTTPStatus.BAD_REQUEST
    
    # Validate required fields
    required_fields = ['id', 'name', 'email']
    if not all(field in user_data for field in required_fields):
        missing_field = next((field for field in required_fields if field not in user_data), None)
        return jsonify({'error': f'Missing required field: {missing_field}'}), HTTPStatus.BAD_REQUEST
    
    try:
        # Get database connection
        session = get_db_connection()
        
        # Insert user into database
        query = "INSERT INTO users (id, name, email) VALUES (?, ?, ?)"
        session.execute(query, (user_data['id'], user_data['name'], user_data['email']))
        
        # Return success response
        return jsonify({'message': 'User added successfully'}), HTTPStatus.CREATED
    except Exception as e:
        # Log error and return error response
        app.logger.error(f'Error adding user: {str(e)}')
        return jsonify({'error': 'An error occurred while adding the user'}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        # Ensure database connection is closed even if an error occurs
        if 'session' in locals():
            session.shutdown()


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()


class TestDatabaseOperationEndpoint(BaseTestCase):
    def _mock_db_response(self, return_value=None, side_effect=None):
        """Helper method to mock database connections"""
        patcher = unittest.mock.patch('sqlite3.connect')
        mock_connect = patcher.start()
        self.addCleanup(patcher.stop)
        
        if side_effect:
            mock_connect.side_effect = side_effect
            return mock_connect
            
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = return_value or []
        return mock_connect
        
    def test_database_operation_success(self):
        # Mock the database response
        self._mock_db_response([(1, 'John'), (2, 'Jane')])
        
        response = self.app.get('/database_operation')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [(1, 'John'), (2, 'Jane')])
        
    def test_database_operation_no_data(self):
        # Mock the database response with no data
        self._mock_db_response([])
        
        response = self.app.get('/database_operation')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'message': 'No data found'})

    def test_database_operation_error(self):
        # Mock a database error
        self._mock_db_response(side_effect=sqlite3.Error('Database error'))
        
        response = self.app.get('/database_operation')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {
                         'error': 'Database error occurred'})


class TestAddUserEndpoint(BaseTestCase):
    # Inheriting setUp from BaseTestCase

    def test_add_user_success(self):
        # Mock the ScyllaDB session and successful user insertion
        with unittest.mock.patch('cassandra.cluster.Cluster') as mock_cluster:
            mock_session = mock_cluster.return_value.connect.return_value
            mock_session.execute.return_value = None

            user_data = {
                'id': 1,
                'name': 'John Doe',
                'email': 'john@example.com'
            }
            response = self.app.post('/add_user', json=user_data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.get_json(), {'message': 'User added successfully'})

    def test_add_user_missing_fields(self):
        user_data = {
            'name': 'John Doe'
        }
        response = self.app.post('/add_user', json=user_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {
                         'error': 'Missing required field: id'})

    def test_add_user_error(self):
        # Mock an error during user insertion
        with unittest.mock.patch('cassandra.cluster.Cluster') as mock_cluster:
            mock_session = mock_cluster.return_value.connect.return_value
            mock_session.execute.side_effect = Exception('Database error')

            user_data = {
                'id': 1,
                'name': 'John Doe',
                'email': 'john@example.com'
            }
            response = self.app.post('/add_user', json=user_data)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.get_json(), {
                             'error': 'An error occurred while adding the user'})


# Utility functions for consistent response handling

def create_response(data, status_code=200):
    """Create a standardized API response"""
    return jsonify(data), status_code

def error_response(message, status_code=500):
    """Create a standardized error response"""
    app.logger.error(f"Error: {message}")
    return create_response({"error": message}, status_code)

@app.route('/endpoint')
def endpoint():
    try:
        # Endpoint logic
        return create_response({'message': 'Success'})
    except Exception as e:
        return error_response(str(e))
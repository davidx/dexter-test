import logging

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

def create_app(config=None):
    flask_app = Flask(__name__)
    import os
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///users.db')
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SECRET_KEY'] = 'your-secret-key-here'  # Should be loaded from environment variables in production
    
    if config:
        flask_app.config.update(config)
        
    db.init_app(flask_app)
    
    # Initialize Flask-Login
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(flask_app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return flask_app

app = create_app()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

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


import logging

from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize rate limiter
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/users', methods=['POST'])
@limiter.limit("5 per minute")
def create_user():
    data = request.get_json()
    
    if not data or not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate email format
    if not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
        
    # Validate password strength
    if not is_strong_password(data['password']):
        return jsonify({'error': 'Password too weak'}), 400
        
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
        
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

# Helper functions for validation
import re


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    # At least 8 chars, contains uppercase, lowercase, number, and special char
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c in '!@#$%^&*()_-+={}[]|:;<>,.?/~`' for c in password):
        return False
    return True


@app.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limit maximum per_page to prevent abuse
    per_page = min(per_page, 100)
    
    try:
        pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
        users = pagination.items
        
        return jsonify({
            'users': [user.to_dict() for user in users],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        })
    except Exception as e:
        app.logger.error(f"Pagination error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve users'}), 500
    # This duplicate code should be removed as it's already handled in the try block


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Implement proper authentication
    # Move this import to the top of the file with other imports
    
    if not current_user.is_authenticated or current_user.id != user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'username' in data:
        if User.query.filter_by(username=data['username']).first() and data['username'] != user.username:
            return jsonify({'error': 'Username already exists'}), 400
        user.username = data['username']
        
    if 'email' in data:
        if User.query.filter_by(email=data['email']).first() and data['email'] != user.email:
            return jsonify({'error': 'Email already exists'}), 400
        user.email = data['email']
        
    if 'password' in data:
        user.set_password(data['password'])
    
    db.session.commit()
    return jsonify(user.to_dict())


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Implement proper authentication
    # Move this import to the top of the file with other imports
    
    if not current_user.is_authenticated or current_user.id != user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})


import unittest


class TestDataEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_data_endpoint(self):
        response = self.app.get('/data')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [1, 2, 3, 4, 5])


def main():
    try:
        with app.app_context():
            db.create_all()
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        logging.error(
            f"Failed to start Flask app due to {str(e)}", exc_info=True)

if __name__ == '__main__':
    main()


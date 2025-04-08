import logging

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    if config:
        app.config.update(config)
        
    db.init_app(app)
    
    return app

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


from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Add to imports and initialize with app
# limiter = Limiter(app, key_func=get_remote_address)

@app.route('/users', methods=['POST'])
# @limiter.limit("5 per minute")
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
def is_valid_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    # At least 8 chars, contains uppercase, lowercase, number, and special char
    if len(password) < 8:
        return False
    return True  # Simplified for example


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
    users = pagination.items
    
    return jsonify({
        'users': [user.to_dict() for user in users],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Implement proper authentication
    from flask_login import current_user, login_required
    
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
    from flask_login import current_user, login_required
    
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


@app.route('/endpoint')
def endpoint():
    try:
        # Endpoint logic
        return jsonify({'message': 'Success'}), 200
    except Exception as e:
        return jsonify({'error': 'Error occurred', 'details': str(e)}), 500
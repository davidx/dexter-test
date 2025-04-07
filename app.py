from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health_check():
    from flask import jsonify

    return jsonify({
        'status': 'healthy',
        'message': 'Service is up and running'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)

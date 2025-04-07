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

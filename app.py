def health_check():
    try:
        status = {"status": "healthy", "message": "Service is up and running"}
        return jsonify(status), 200
    except Exception as e:
        app.logger.error(f"Health Check Error: {str(e)}")
        error = {"status": "unhealthy", "error": str(e)}
        return jsonify(error), 500
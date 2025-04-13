def database_operation():
    conn = None
    try:
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM example_table')
        result = cursor.fetchall()

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
    finally:
        if conn:
            conn.close()
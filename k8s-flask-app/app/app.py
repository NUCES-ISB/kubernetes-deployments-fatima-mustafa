from flask import Flask, jsonify
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import socket

app = Flask(__name__)

# Get database connection details from environment variables
DB_USER = os.environ.get('DB_USER', 'postgresuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgrespassword')
DB_NAME = os.environ.get('DB_NAME', 'flaskapp')
DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_PORT = os.environ.get('DB_PORT', '5432')

# Create the database URI
DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

@app.route('/')
def index():
    hostname = socket.gethostname()
    return jsonify({
        "message": "Flask app is running!",
        "hostname": hostname,
        "pod_ip": socket.gethostbyname(hostname)
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/db-check')
def db_check():
    try:
        engine = create_engine(DATABASE_URI)
        connection = engine.connect()
        
        # Test query to check if connection is working
        result = connection.execute(text("SELECT 1"))
        connection.close()
        
        return jsonify({
            "status": "success",
            "message": "Connected to PostgreSQL database successfully!"
        })
    except OperationalError as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to connect to PostgreSQL database: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, request, jsonify
from waitress import serve
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.security import generate_password_hash

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection setup
uri = "mongodb+srv://hipo:hipo@hipo.ia7ctsa.mongodb.net/?retryWrites=true&w=majority&appName=HiPo"
client = MongoClient(uri, server_api=ServerApi('1'))

# Check connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Database and collection
db = client['user_database']
collection = db['users']

# Define the API endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    user_data = {
        "email": email,
        "password": hashed_password
    }

    # Store the user data in MongoDB
    try:
        insert_result = collection.insert_one(user_data)
        user_data["_id"] = str(insert_result.inserted_id)
        return jsonify(user_data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app with Waitress
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)

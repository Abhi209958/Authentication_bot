from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
# Try to load .env file from current directory
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"Loading .env from: {env_path}")
load_dotenv(env_path)

# Debug: Print current directory and check if .env file exists
print(f"Current working directory: {os.getcwd()}")
print(f".env file exists: {os.path.exists(env_path)}")

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# MongoDB connection
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
print(f"MongoDB URI loaded: {'Yes' if mongodb_uri else 'No'}")
mongo_client = MongoClient(mongodb_uri)
db = mongo_client['auth_db']  # Using auth_db as specified in your Atlas URI
users_collection = db['users']
chats_collection = db['chats']

# Gemini AI configuration
gemini_api_key = os.getenv('GEMINI_API_KEY')
print(f"Gemini API Key loaded: {'Yes' if gemini_api_key else 'No'}")

gemini_model = None

if gemini_api_key:
    print(f"API Key starts with: {gemini_api_key[:10]}...")
    try:
        genai.configure(api_key=gemini_api_key)
        
        # Use Gemini 2.5 Flash model
        gemini_model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ Gemini 2.5 Flash initialized successfully!")
            
    except Exception as e:
        print(f"❌ Error configuring Gemini API: {e}")
        gemini_model = None
else:
    print("WARNING: GEMINI_API_KEY not found in environment variables!")
    print("Please add your Gemini API key to the .env file.")

# Routes
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if not email or not password or not name:
            return jsonify({'error': 'All fields are required'}), 400
        
        # Check if user already exists
        if users_collection.find_one({'email': email}):
            return jsonify({'error': 'User already exists'}), 400
        
        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create user
        user = {
            'name': name,
            'email': email,
            'password': hashed_password,
            'created_at': datetime.utcnow()
        }
        
        result = users_collection.insert_one(user)
        
        # Create access token
        access_token = create_access_token(identity=str(result.inserted_id))
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': {
                'id': str(result.inserted_id),
                'name': name,
                'email': email
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user
        user = users_collection.find_one({'email': email})
        
        if not user or not bcrypt.check_password_hash(user['password'], password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create access token
        access_token = create_access_token(identity=str(user['_id']))
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
@jwt_required()
def chat():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Check if Gemini is configured
        if not gemini_model:
            return jsonify({'error': 'Gemini AI not configured properly'}), 500
        
        # Create prompt with system instructions
        full_prompt = f"""You are a helpful AI assistant with access to the latest information and data. Provide clear, concise, and helpful responses. You have up-to-date knowledge and can help with current topics and recent developments.

User question: {message}

Please provide a comprehensive and helpful response:"""
        
        # Call Gemini API with simpler configuration for free tier
        response = gemini_model.generate_content(
            full_prompt,
            generation_config={
                'max_output_tokens': 800,  # Reduced for free tier
                'temperature': 0.7,
            }
        )
        
        ai_response = response.text
        
        # Save chat to database
        chat = {
            'user_id': current_user_id,
            'user_message': message,
            'ai_response': ai_response,
            'timestamp': datetime.utcnow()
        }
        
        chats_collection.insert_one(chat)
        
        return jsonify({
            'response': ai_response
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat-history', methods=['GET'])
@jwt_required()
def get_chat_history():
    try:
        current_user_id = get_jwt_identity()
        
        chats = list(chats_collection.find(
            {'user_id': current_user_id},
            {'_id': 0}
        ).sort('timestamp', -1).limit(50))
        
        return jsonify({'chats': chats}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        current_user_id = get_jwt_identity()
        user = users_collection.find_one({'_id': ObjectId(current_user_id)})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

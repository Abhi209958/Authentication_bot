from pymongo import MongoClient
from datetime import datetime

def init_database():
    """Initialize MongoDB database and collections"""
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['auth_system']
        
        # Create collections if they don't exist
        users_collection = db['users']
        chats_collection = db['chats']
        
        # Create indexes for better performance
        users_collection.create_index('email', unique=True)
        chats_collection.create_index('user_id')
        chats_collection.create_index('timestamp')
        
        print("Database initialized successfully!")
        print("Collections created: users, chats")
        print("Indexes created for better performance")
        
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_database()

# ChatBot Authentication System

A full-stack application with React frontend and Flask backend featuring user authentication and ChatGPT-like interface.

## Features

- User registration and login
- JWT-based authentication
- ChatGPT-like interface using Google Gemini AI
- Chat history storage in MongoDB
- Modern, responsive UI with Tailwind CSS

## Setup Instructions

### Backend Setup

1. Navigate to the Backend directory:
   ```bash
   cd Backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the Backend directory and add your configuration:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   MONGODB_URI=mongodb://localhost:27017/
   JWT_SECRET_KEY=your_jwt_secret_key_here
   ```

6. Make sure MongoDB is running on your system

7. Run the Flask application:
   ```bash
   python app.py
   ```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the Authenticatesystem directory:
   ```bash
   cd Authenticatesystem
   ```

2. Install dependencies (if not already done):
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## Usage

1. Open your browser and go to `http://localhost:5173`
2. Register a new account or login with existing credentials
3. Start chatting with the AI after successful authentication
4. Your chat history will be saved and restored when you log back in

## Technologies Used

### Frontend
- React 19
- React Router DOM
- Axios for API calls
- Tailwind CSS for styling
- Vite for build tooling

### Backend
- Flask
- Flask-CORS
- Flask-BCrypt for password hashing
- Flask-JWT-Extended for authentication
- PyMongo for MongoDB integration
- Google Gemini AI for intelligent responses
- Python-dotenv for environment variables

### Database
- MongoDB for user data and chat history storage

## API Endpoints

- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/chat` - Send message to AI
- `GET /api/chat-history` - Get user's chat history
- `GET /api/profile` - Get user profile

## Environment Variables

Create a `.env` file in the Backend directory with the following variables:

```
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URI=mongodb://localhost:27017/
JWT_SECRET_KEY=your_jwt_secret_key_here
```

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Protected API routes
- CORS configuration
- Input validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

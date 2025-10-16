"""
Test script to check if Gemini API is working correctly
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

print("Testing Gemini API integration...")
print("=" * 50)

# Load environment variables
load_dotenv()

# Get API key
gemini_api_key = os.getenv('GEMINI_API_KEY')

print(f"Gemini API Key: {'✅ Found' if gemini_api_key else '❌ Not found'}")

if gemini_api_key and gemini_api_key != 'your_gemini_api_key_here':
    print(f"API Key starts with: {gemini_api_key[:10]}...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        
        # Initialize model
        model = genai.GenerativeModel('gemini-pro')
        print("✅ Gemini model initialized successfully!")
        
        # Test with a simple question
        print("\nTesting with a sample question...")
        response = model.generate_content("What are the latest developments in AI in 2024?")
        
        print("✅ Test successful!")
        print(f"Response preview: {response.text[:200]}...")
        
    except Exception as e:
        print(f"❌ Error testing Gemini API: {e}")
        print("\nPlease check:")
        print("1. Your Gemini API key is correct")
        print("2. You have enabled the Generative AI API in Google Cloud Console")
        print("3. Your API key has the necessary permissions")
        
else:
    print("❌ Please add your Gemini API key to the .env file")
    print("\nTo get a Gemini API key:")
    print("1. Go to https://makersuite.google.com/app/apikey")
    print("2. Create a new API key")
    print("3. Add it to your .env file as GEMINI_API_KEY=your_key_here")

print("\n" + "=" * 50)

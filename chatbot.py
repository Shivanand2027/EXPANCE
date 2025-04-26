from flask import Blueprint, jsonify, request
import os
import requests
from dotenv import load_dotenv

# Load environment variables (optional here if loaded in app.py, but doesn't hurt)
load_dotenv()

# Create Blueprint
chat = Blueprint('chat', __name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
print(f"Loaded API Key: {GEMINI_API_KEY}")  # Debug print
API_VERSION = "v1beta"  # Changed to v1beta to match working test
MODEL = "gemini-2.0-flash"  # Changed to match working test
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/{API_VERSION}/models/{MODEL}:generateContent"

# Define travel assistant context and sample responses
SAMPLE_RESPONSES = {
    'greetings': 'Hello! I am your Travel Assistant. How can I help you today?',
    'default': 'I understand you need help with travel planning. Could you please provide more specific details about what you need assistance with? I can help with trip planning, destinations, travel tips, or expense management.',
    'error': 'I apologize, but I am currently operating in a limited capacity. However, I can still provide basic travel assistance and information.',
    'expense': 'I can help you manage your travel expenses. You can add expenses, view your spending history, and manage group expenses through our platform.',
    'trip': 'Let me help you plan your trip. I can assist with destination recommendations, itinerary planning, and travel tips.',
    'help': 'I can help you with: \n1. Travel expense management\n2. Trip planning\n3. Group expense sharing\n4. Travel recommendations'
}

def get_gemini_response(message):
    api_key = os.getenv('GEMINI_API_KEY')
    print(f"--- Using API Key in get_gemini_response: {api_key}") # Debug print full key

    if not api_key:
        print("--- ERROR: GEMINI_API_KEY not found in environment!")
        return SAMPLE_RESPONSES['error']

    try:
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Simplified request payload structure to match working test
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": f"You are a travel expense assistant. Help the user with their query: {message}"}
                    ]
                }
            ]
        }

        print(f"--- Sending request to Gemini API URL: {GEMINI_API_URL}") # Debug print
        response = requests.post(
            f"{GEMINI_API_URL}?key={api_key}",
            headers=headers,
            json=data,
            timeout=30 # Add a timeout
        )

        print(f"--- Gemini API Status Code: {response.status_code}") # Debug print
        print(f"--- Gemini API Response: {response.text}") # Debug print
        
        if response.status_code != 200:
            print(f"--- Error Response: {response.text}")
            return f"Error: {response.status_code} - {response.text}"

        result = response.json()
        
        # Simplified response parsing to match working test
        if 'candidates' in result and result['candidates']:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                parts = candidate['content']['parts']
                if parts and 'text' in parts[0]:
                    return parts[0]['text']

        print("--- ERROR: Unexpected response structure from Gemini API.") # Debug print
        print(f"--- Full Response JSON: {result}") # Debug print
        return SAMPLE_RESPONSES['error']

    except requests.exceptions.RequestException as e: # Catch specific request errors
        print(f"--- Gemini API Request Exception: {str(e)}") # Debug print
        return f"API Error: {str(e)}"
    except Exception as e:
        print(f"--- Unexpected error in get_gemini_response: {str(e)}") # Debug print
        return f"Error: {str(e)}"


@chat.route('/chat', methods=['POST'])
def handle_chat():
    try:
        # Validate request data
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
            
        user_message = request.json.get('message')
        if not user_message or not isinstance(user_message, str):
            return jsonify({'error': 'Please provide a valid message'}), 400

        if len(user_message.strip()) == 0:
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Get response from Gemini API
        response = get_gemini_response(user_message)

        return jsonify({
            'response': response
        })

    except Exception as e:
        print(f"Chat error: {str(e)}")
        return jsonify({
            'error': f'An unexpected error occurred: {str(e)}'
        }), 500
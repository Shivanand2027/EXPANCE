import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key loaded: {api_key}")

# Check if .env file exists
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(f".env file exists: {os.path.exists(env_path)}")

# Print all environment variables (be careful with sensitive data)
print("\nAll environment variables:")
for key, value in os.environ.items():
    if 'API' in key or 'KEY' in key:
        print(f"{key}: {value[:5]}...") 
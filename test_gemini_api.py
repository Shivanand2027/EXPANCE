import requests
import json

API_KEY = "AIzaSyAymNvGdRh_FAM0zXcJLWR-UqLMsjsVD1U"  # Replace this with your key, e.g., AIzaSyD...VD1U

MODEL = "gemini-2.0-flash"
API_VERSION = "v1beta"  # Important: you're using v1beta here

def ask_gemini(question):
    url = f"https://generativelanguage.googleapis.com/{API_VERSION}/models/{MODEL}:generateContent?key={API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {"text": question}
                ]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    print("Status Code:", response.status_code)
    
    try:
        result = response.json()
        # Extract the text response from the Gemini API response
        if "candidates" in result and len(result["candidates"]) > 0:
            if "content" in result["candidates"][0] and "parts" in result["candidates"][0]["content"]:
                if len(result["candidates"][0]["content"]["parts"]) > 0 and "text" in result["candidates"][0]["content"]["parts"][0]:
                    return result["candidates"][0]["content"]["parts"][0]["text"]
        
        # If we couldn't extract the text, return the full response
        return json.dumps(result, indent=2)
    except json.JSONDecodeError:
        return f"Failed to decode JSON response: {response.text}"

# Example usage
if __name__ == "__main__":
    question = input("Enter your question for Gemini: ")
    response = ask_gemini(question)
    print("\nGemini's response:")
    print(response)

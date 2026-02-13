from google import genai
import os

def test_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        return

    client = genai.Client(api_key=api_key)
    
    print("--- Listing Available Models ---")
    try:
        # In the new google-genai SDK, models.list() returns an iterator
        for model in client.models.list():
            print(f"Model ID: {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

    print("\n--- Testing Content Generation with gemini-1.5-flash ---")
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="Hello, this is a diagnostic test."
        )
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Failed with gemini-1.5-flash: {e}")

    print("\n--- Testing Content Generation with gemini-1.5-flash-latest ---")
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents="Hello, this is a second diagnostic test."
        )
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Failed with gemini-1.5-flash-latest: {e}")

if __name__ == "__main__":
    test_gemini()

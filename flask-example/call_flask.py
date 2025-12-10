import requests
import time
import sys

def call_flask_app(city="Paris, France"):
    url = "http://localhost:5001/generate_city_guide"
    payload = {"city": city}
    
    print(f"Calling Flask app for {city}...")
    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            print(f"\nSuccess! (Time: {elapsed:.2f}s)")
            print("Response:", response.json())
        else:
            print(f"\nFailed! (Status: {response.status_code})")
            print("Error:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to Flask app. Is it running on port 5001?")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    city = sys.argv[1] if len(sys.argv) > 1 else "Milan, Italy"
    call_flask_app(city)

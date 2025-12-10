import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# STANDARD FLASK TIMEOUT IS OFTEN 60s
# BROWSERS/NGINX OFTEN TIMEOUT AT 60s

@app.route("/generate_city_guide", methods=["POST"])
def generate_city_guide():
    data = request.json
    city = data.get("city")
    
    # 1. This is a BLOCKING call.
    # If GPT-4 takes 65 seconds, the client (browser) disconnects.
    # If the server restarts during this line, the request is lost.
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Slow, expensive model
            messages=[
                {"role": "system", "content": "You are a travel agent. Create a detailed 3-day itinerary including weather checks."},
                {"role": "user", "content": f"Plan a trip to {city}."}
            ],
            timeout=30.0 # <--- THE BUG. We set a timeout to "fail fast", but AI needs time.
        )
        
        itinerary = response.choices[0].message.content
        
        # 2. Database write (What if this fails after we paid for the AI?)
        # save_to_db(itinerary) 
        
        return jsonify({"itinerary": itinerary})

    except Exception as e:
        # 3. No easy way to retry just the AI part without re-running the whole request
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001)
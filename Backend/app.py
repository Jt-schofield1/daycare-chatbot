from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load OpenAI API key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization="org-V3A5isksgXaG4xuOhAiYjzee"

    )

# Predefined FAQ responses
FAQ = {
    "what are your hours of operation?": "Our daycare is open from 7:00 AM to 6:00 PM, Monday through Friday.",
    "what is your tuition fee?": "Our monthly tuition starts at $800. Please contact us for more details.",
    "what is your sick child policy?": "If your child has a fever or contagious illness, we request they stay home until symptom-free for 24 hours.",
    "how can i schedule a tour?": "You can schedule a tour by calling us at (123) 456-7890 or filling out the form on our website.",
    "do you provide meals?": "Yes, we provide healthy meals and snacks throughout the day, including options for allergies."
}

# Load dynamic data (e.g., waitlist count) from JSON file
def get_dynamic_data(key):
    try:
        with open("config.json", "r") as file:
            data = json.load(file)
        return data.get(key, "Information not available")
    except Exception as e:
        return f"Error fetching data: {str(e)}"

# Chatbot endpoint
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    # Check for dynamic data queries (e.g., waitlist status)
    if "waitlist" in user_message:
        waitlist_count = get_dynamic_data("waitlist")
        return jsonify({"reply": f"The current waitlist has {waitlist_count} students."})

    # Check FAQ for a static response
    for question, answer in FAQ.items():
        if question in user_message:
            return jsonify({"reply": answer})

    # If question is not in FAQ, call OpenAI API for response
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are an AI assistant for Little Acorns Learning Center. Answer questions accurately about daycare policies, hours, tuition, and other common inquiries."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=100,
            temperature=0.7
        )
        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("OpenAI API Error:", str(e))  # Logs error to the server
        return jsonify({"reply": "Sorry, I'm having trouble right now.", "error": str(e)}), 500

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)

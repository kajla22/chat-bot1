from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Azure OpenAI Configuration
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  # This should not include "/completions"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]

    try:
        # Corrected API call with 'deployment_id'
        response = openai.ChatCompletion.create(
            deployment_id=os.getenv("AZURE_OPENAI_DEPLOYMENT"),  # Pass deployment_id here
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        print("API Response:", response)  # Print the full response for debugging
        return response['choices'][0]['message']['content'].strip()
        
    except Exception as e:
        print("Error during API call:", str(e))  # Log any errors
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
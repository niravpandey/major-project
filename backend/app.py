import os
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv

load_dotenv()

# Set up your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend_courses():
    user_input = request.json.get('user_input')

    if not user_input:
        return jsonify({'error': 'No user input provided'}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150
        )
        
        courses = response['choices'][0]['message']['content'].strip()
        
        return jsonify({'courses': courses}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

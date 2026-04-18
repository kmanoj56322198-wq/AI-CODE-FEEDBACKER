import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure API Key securely via environment variable
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app) 

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'AI Code Reviewer API is running!',
        'endpoints': {
            '/api/feedback': 'POST - Get AI feedback on code snippets'
        }
    })

@app.route('/api/feedback', methods=['POST'])
def get_code_feedback():
    data = request.json
    user_code = data.get('code', '')
    language = data.get('language', 'javascript')

    if not user_code.strip():
        return jsonify({'error': 'No code provided.'}), 400
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        You are an expert code reviewer. Analyze the following {language} code and provide detailed feedback using markdown format:
        1. Readability
        2. Performance
        3. Bugs or edge cases
        
        Feel free to write the suggested code improvements as well.

        Code:
        {user_code}
        """
        response = model.generate_content(prompt)
        ai_feedback_text = response.text
    except Exception as e:
        print("Error with Gemini API:", e)
        ai_feedback_text = "Error generating feedback. Have you configured your GEMINI_API_KEY in the backend?"

    return jsonify({
        'feedback': ai_feedback_text,
        'status': 'success'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot_2 import ask_ai as chatbot_ask_ai

port_no = 5000
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Authorization", "Content-Type"]}})

@app.route('/ask', methods=['POST'])
def ask():
    # Extract question from the request
    data = request.json
    question = data.get('question')
    
    # Check if a question is provided
    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Generate response using the chatbot function
    response = chatbot_ask_ai(question)
    
    print(response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

# OpenAI API 키 설정
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',  # 사용할 모델 설정
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=1024,  # 반환되는 텍스트 길이를 늘림 (최대 4096)
            n=1,
            stop=None,
            temperature=0.5
        )
        bot_response = response.choices[0].message['content'].strip()
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

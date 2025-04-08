import openai
import requests
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# OpenAI API 키를 환경 변수에서 불러오기
openai.api_key = os.getenv('OPENAI_API_KEY')

# Flask 서버로 POST 요청을 보내는 함수 (서버 열기 위한 명령어 -> flask run)
def send_to_flask(user_input):
    url = 'http://127.0.0.1:5000/chat'  # Flask 서버 주소
    data = {'message': user_input}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()['reply']  # 서버에서 받은 응답
    else:
        print(f"Error: {response.status_code}")
        return "Error occurred"

# GPT-4 응답 생성 함수
def get_neo_response(user_input):
    response = openai.Completion.create(
        model="gpt-4",  # GPT-4 모델 사용
        prompt=user_input,
        max_tokens=150
    )
    print("GPT-4 Response:", response.choices[0].text.strip())  # 응답 로그 추가
    return response.choices[0].text.strip()

# 사용자 입력을 받아서 Flask 서버로 전달 후 응답 받기
def handle_user_input(user_input):
    # Flask 서버에서 처리된 응답을 받아오기
    flask_response = send_to_flask(user_input)
    return flask_response

if __name__ == "__main__":
    user_input = input("Enter your message: ")
    response = handle_user_input(user_input)
    print("Response from Flask:", response)

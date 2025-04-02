from flask import Flask # Flask 모듈 임포트

app = Flask(__name__) # Flask 웹 애플리케이션 생성 

@app.route("/hello", methods=['GET']) # '/hello' 엔드포인트를 GET 방식으로 요청
def hello(): # 함수 정의
  return "hello world" # 반환하여 출력

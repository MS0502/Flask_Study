from flask import Flask, render_template, request, redirect # 필요한 모듈 import
import os # 운영체제에서 제공되는 여러 기능을 파이썬에서 수행할 수 있게 해주는 모듈
from pymongo import MongoClient
import re # 이메일 형식 체크를 위한 모듈

app = Flask(__name__) # Flask 웹 애플리케이션 생성

# MongoDB 클라이언트 연결
client = MongoClient('127.0.0.1', 27017)  # 127.0.0.1 => 몽고 DB 로컬 IP / 27017 => 포트번호

# MongoDB 데이터베이스, 컬랙션 생성 및 연결
db = client["admin"]
collection = db['user_database']

@app.route('/')
def home(): # 메인 함수 정의 (Flask 가 실행되자마자 1순위로)
    return render_template('index.html') # 유저에게 보여지게 되는 웹 페이지 렌더링

# 로그인 API (로그인 페이지 접속 (GET) 처리와, act
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_id = request.form['user_id']
        try:
            user = collection.find_one({'user_id': user_id})

            if user is not None:
                print("비밀번호 일치")
                return redirect('/')
            else:
                return '아이디 또는 비밀번호가 잘못되었습니다.'
        except Exception as e:
            return f'예외 발생: {str(e)}'  # 예외 상황에 대한 더 구체적인 메시지

# 회원가입 API
@app.route('/register', methods=['GET','POST'])
def register():  # 함수 생성
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # 회원정보 생성
        user_id = request.form.get('user_id')  # 유저 아이디 (아이디 중복체크)
        user_name = request.form.get('user_name')  # 유저 이름
        user_password = request.form.get('user_password')  # 유저 비밀번호
        user_re_password = request.form.get('user_re_password')  # 비밀번호가 동일하지 않을 경우)
        user_email = request.form.get('user_email')  # 유저 메일 (@이나 이메일 형식이 올바르지 않을 경우)

        # 비밀번호 확인
        if user_password != user_re_password:
            return "비밀번호가 일치하지 않습니다. 다시 입력해주세요."

        # 이메일 형식 체크 (정규식 사용)
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, user_email):
            return "잘못된 이메일 형식입니다. 다시 입력해주세요."

        # 데이터베이스에 저장할 사용자 정보
        user_data = {
            'user_id': user_id,
            'user_name': user_name,
            'user_password': user_password,
            'user_re_password': user_re_password,
            'user_email': user_email
        }

        try:
            client.admin.command('ping')
            print("MongoDB 연결 성공!")
        except Exception as e:
            print(f"MongoDB 연결 실패: {e}")

        # 중복 체크 및 입력 필드에 입력 값 존재 여부 구현

        # 데이터베이스 collection에 사용자 데이터 삽입
        collection.insert_one(user_data)

        return redirect('/login')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True) #포트번호는 기본 5000, 개발단계에서는 debug는 True
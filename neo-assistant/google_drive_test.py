from google_auth_oauthlib.flow import InstalledAppFlow
import os.path

# 필요한 권한 설정
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def main():
    # OAuth 2.0 클라이언트 비밀 파일 경로
    creds = None
    if os.path.exists('token.json'):
        print("이미 인증됨 (token.json 존재)")
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret_974203755466-m1pg5td2kv42ieb74sghbq0c1jbgil7s.apps.googleusercontent.com.json', SCOPES)
        creds = flow.run_local_server(port=0)

        # 인증 완료되면 token 저장
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            print("인증 성공! token.json 저장 완료")

if __name__ == '__main__':
    main()

import os
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def create_drive_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("drive", "v3", credentials=creds)

def get_or_create_folder(service, folder_name):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
    folders = results.get("files", [])

    if folders:
        return folders[0]["id"]

    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    folder = service.files().create(body=file_metadata, fields="id").execute()
    return folder.get("id")

def upload_file(service, folder_id, file_path, file_name=None):
    file_metadata = {
        "name": file_name if file_name else os.path.basename(file_path),
        "parents": [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)

    # 이미 존재하는 파일이 있으면 덮어쓰기
    files = service.files().list(
        q=f"name='{file_metadata['name']}' and '{folder_id}' in parents",
        spaces='drive',
        fields='files(id, name)'
    ).execute().get('files', [])

    if files:
        file_id = files[0]['id']
        service.files().update(fileId=file_id, media_body=media).execute()
        print(f"기존 파일 덮어쓰기 완료: {file_metadata['name']}")
    else:
        service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        print(f"새 파일 업로드 완료: {file_metadata['name']}")

def download_file(service, folder_id, file_name):
    try:
        query = f"name='{file_name}' and '{folder_id}' in parents"
        results = service.files().list(
            q=query,
            spaces="drive",
            fields="files(id, name)"
        ).execute()

        items = results.get("files", [])
        if not items:
            print(f"{file_name} 파일이 존재하지 않습니다.")
            return

        file_id = items[0]["id"]
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(file_name, "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        print(f"{file_name} 다운로드 완료.")
    except HttpError as error:
        print(f"파일 다운로드 중 오류 발생: {error}")


import os
import boto3
from botocore.config import Config
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv
from fastapi import File, HTTPException, UploadFile

load_dotenv(override=True)

R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_ENDPOINT = os.getenv("R2_ENDPOINT")


s3_client = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    config=Config(signature_version="s3v4")
)


async def upload_file(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        file_key = f"uploads/{file.filename}"

        s3_client.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=file_key,
            Body=file_content,
            ContentType=file.content_type
        )

        return {"message": "File uploaded successfully", "file_key": file_key}
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise HTTPException(status_code=500, detail="Invalid R2 credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

def list_files():
    response = s3_client.list_objects_v2(Bucket=R2_BUCKET_NAME)

    if "Contents" not in response:
            return {"message": "No files found in the bucket", "files": []}

    return {"message": "Files listed successfully", "files": response}


def get_video_with_key(key: str):
# Key = nome do arquivo + extensão -> teste.mkv
    try:  
        response = s3_client.head_object(Bucket=R2_BUCKET_NAME, Key=key)
        
        return {
             'video': {
                  'key': key,
                  'lastModified': response['LastModified'],
                  'size': response['ContentLength'],
                  'url': f"{os.getenv('R2_ENDPOINT')}/{R2_BUCKET_NAME}/{key}"
             }
        }
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")


def delete_video_from_cloud(key: str):
    try:
        s3_client.delete_object(Bucket=R2_BUCKET_NAME, Key=key)

    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")




import aioboto3
from app.config import settings


async def upload_file_to_s3(file_bytes: bytes, file_name: str, content_type: str):
    session = aioboto3.Session()

    async with session.client(
        service_name = "s3",
        endpoint_url = settings.s3_endpoint_url,
        aws_access_key_id = settings.s3_access_key,
        aws_secret_access_key = settings.s3_secret_key,
        region_name = 'ru-central1'
    ) as s3_client:
        
        await s3_client.put_object(
            Bucket = settings.s3_bucket_name,
            Key = file_name,
            Body = file_bytes,
            ContentType = content_type
        )

    
async def get_presigned_url(file_name: str, expiration: int = 900) -> str:
    session = aioboto3.Session()

    async with session.client(
        service_name = "s3",
        endpoint_url = settings.s3_endpoint_url,
        aws_access_key_id = settings.s3_access_key,
        aws_secret_access_key = settings.s3_secret_key,
        region_name = 'ru-central1'
    ) as s3_client:
        
        url = await s3_client.generate_presigned_url(
            "get_object",
            Params = {
                "Bucket": settings.s3_bucket_name,
                "Key": file_name
            },
            ExpiresIn = expiration
        )
        
        return url
    

async def download_file_from_s3(file_key: str) -> bytes:
    session = aioboto3.Session()

    async with session.client(
        service_name = "s3",
        endpoint_url = settings.s3_endpoint_url,
        aws_access_key_id = settings.s3_access_key,
        aws_secret_access_key = settings.s3_secret_key,
        region_name = 'ru-central1'
    ) as s3_client:

        response = await s3_client.get_object(
            Bucket = settings.s3_bucket_name,
            Key = file_key
        )

        file_bytes = await response["Body"].read()
        return file_bytes

async def delete_file_from_s3(file_key: str):
    session = aioboto3.Session()

    async with session.client(
        service_name = "s3",
        endpoint_url = settings.s3_endpoint_url,
        aws_access_key_id = settings.s3_access_key,
        aws_secret_access_key = settings.s3_secret_key,
        region_name = 'ru-central1'
    ) as s3_client:
        await s3_client.delete_object(
            Bucket=settings.s3_bucket_name,
            Key=file_key
        )

    
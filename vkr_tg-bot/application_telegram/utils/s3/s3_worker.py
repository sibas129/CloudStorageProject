import boto3
from botocore.exceptions import NoCredentialsError
from config import S3_URL, S3_PUBLIC_KEY, S3_PRIVATE_KEY


class S3Worker:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=S3_PUBLIC_KEY,
            aws_secret_access_key=S3_PRIVATE_KEY,
            endpoint_url=S3_URL,
        )

    def create_file(
        self, path: str, content: bytes, bucket_name: str = "rucloud"
    ) -> None:
        if not isinstance(content, bytes):
            raise TypeError("Content must be of type bytes")
        try:
            self.s3.put_object(Bucket=bucket_name, Key=path, Body=content)
        except NoCredentialsError:
            raise RuntimeError("Invalid S3 credentials")

    def delete_file(self, path: str, bucket_name: str = "rucloud") -> None:
        try:
            self.s3.delete_object(Bucket=bucket_name, Key=path)
        except NoCredentialsError:
            raise RuntimeError("Invalid S3 credentials")

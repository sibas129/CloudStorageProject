from pydantic_settings import BaseSettings
from pydantic import SecretStr


class AppConfig(BaseSettings):
    SERVER_IP: SecretStr
    ETHERPAD_URL: SecretStr
    TELEGRAM_TOKEN: SecretStr
    DATABASE_HOST: SecretStr
    DATABASE_LOGIN: SecretStr
    DATABASE_PASSWORD: SecretStr
    DATABASE_PORT: int
    DATABASE_NAME: SecretStr
    S3_URL: SecretStr
    S3_PUBLIC_KEY: SecretStr
    S3_PRIVATE_KEY: SecretStr

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


app_config = AppConfig()

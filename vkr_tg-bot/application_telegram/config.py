from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

import asyncio
import functools

from env_reader import app_config


SERVER_IP = app_config.SERVER_IP.get_secret_value()
ETHERPAD_URL = app_config.ETHERPAD_URL.get_secret_value()
TELEGRAM_TOKEN = app_config.TELEGRAM_TOKEN.get_secret_value()
DATABASE_LOGIN = app_config.DATABASE_LOGIN.get_secret_value()
DATABASE_PASSWORD = app_config.DATABASE_PASSWORD.get_secret_value()
DATABASE_PORT = app_config.DATABASE_PORT
DATABASE_NAME = app_config.DATABASE_NAME.get_secret_value()
DATABASE_HOST = app_config.DATABASE_HOST.get_secret_value()
S3_URL = app_config.S3_URL.get_secret_value()
S3_PUBLIC_KEY = app_config.S3_PUBLIC_KEY.get_secret_value()
S3_PRIVATE_KEY = app_config.S3_PRIVATE_KEY.get_secret_value()


database_engine = create_engine(
    f"postgresql+psycopg2://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}",
)
database_engine_async = create_async_engine(
    f"postgresql+asyncpg://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}",
)


def batch_lengh_generator(step: int, data: list) -> list:
    return (data[x : x + step] for x in range(0, len(data), step))


def equal_split(list_to_split, n_parts) -> tuple:
    k, m = divmod(len(list_to_split), n_parts)
    return (
        list_to_split[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)]
        for i in range(n_parts)
    )


def retry_async(num_attempts):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for try_index in range(num_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    print(
                        f"Exception occurred: {e}. Retrying... ({try_index}/{num_attempts})"
                    )
                    await asyncio.sleep(1)
            else:
                print(f"Failed after {num_attempts} attempts.")

        return wrapper

    return decorator

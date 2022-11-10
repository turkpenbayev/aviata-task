from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = 'providers'
    SERVICE_HOST: str = '0.0.0.0'
    SERVICE_PORT: int = 8000

    SLEEP_TIME: int = 5
    SOURCE_FILE: str = './response_b.json'

    class Config:
        case_sensitive = True


settings = Settings()

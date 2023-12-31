from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_DOCKER_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    SQLALCHEMY_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = '.env'


settings = Settings()

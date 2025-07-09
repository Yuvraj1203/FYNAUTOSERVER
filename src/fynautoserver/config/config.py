from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = '.env'

settings = Settings()

print(f"This is config file : {settings.DATABASE_URL}")
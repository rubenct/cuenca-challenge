from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/nqueens_db"
    API_V1_STR: str = "/api/v1"
    TIME_LIMIT: int = 10

    class Config:
        env_file = ".env"

settings = Settings()
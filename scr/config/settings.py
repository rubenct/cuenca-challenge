from pydantic_settings import BaseSettings
"""
Settings in the project:
DATABASE_URL: Variable to read the environment variable whit he string of the database
API_V1_STR: Help versioning application
TIME_LIMIT: Set the max timeout for calculus of solutions in the algorithm
"""

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/nqueens_db"
    API_V1_STR: str = "/api/v1"
    TIME_LIMIT: int = 600

    class Config:
        env_file = ".env"

settings = Settings()
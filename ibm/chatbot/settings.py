from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ibm_api_key: str
    ibm_project_id: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

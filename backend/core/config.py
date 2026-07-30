from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding= "utf-8"
    )
    
    jwt_secret_key : SecretStr
    jwt_algorithm : str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 2
    
    
settings = Settings()
     
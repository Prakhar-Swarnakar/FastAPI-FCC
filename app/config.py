from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    username:str
    password:str
    hostname:str
    port_number:str
    database_name:str
    secret_key:str
    algorithm:str
    access_token_expire_mins: int

    class config():
        env_file = ".env"

settings = Settings()
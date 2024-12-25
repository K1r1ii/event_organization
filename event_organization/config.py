import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_TEST_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_TEST_NAME: str
    DB_USER: str
    DB_TEST_USER: str
    DB_PASS: str
    DB_TEST_PASS: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

    @property
    def get_db_url(self) -> str:
        """DSN базы данных """
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    @property
    def get_test_db_url(self) -> str:
        """ DSN тестовой базы данных """
        return f"mysql+pymysql://{self.DB_TEST_USER}:{self.DB_TEST_PASS}@{self.DB_TEST_HOST}:{self.DB_PORT}/{self.DB_TEST_NAME}"

settings = Settings()
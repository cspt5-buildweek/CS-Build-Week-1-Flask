from os import environ
from dotenv import load_dotenv

load_dotenv()


def get_db_connect_string():
    db_user = environ.get("DB_USER")
    db_password = environ.get("DB_PASS")
    db_host = environ.get("DB_HOST")
    db_port = environ.get("DB_PORT")
    db_name = environ.get("DB_NAME")

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

import os
from sqlalchemy import create_engine


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://demo_user:demo_password@localhost:5432/analytics"
)


engine = create_engine(
    DATABASE_URL
)


def get_connection():

    return engine.connect()
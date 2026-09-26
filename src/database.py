import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine

from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = (
    f"postgresql+psycopg://postgres:{quote_plus(os.getenv('DB_PASSWORD'))}@localhost:5432/customer_support"
)

engine = create_engine(DATABASE_URL)
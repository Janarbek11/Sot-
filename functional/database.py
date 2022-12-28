import os
from sqlalchemy import create_engine, Column, BIGINT, String
from dotenv import load_dotenv
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker

load_dotenv()

host = str(os.getenv("host"))
password = str(os.getenv("db_pass"))
database = str(os.getenv("db_name"))

engine = create_engine(f"postgresql+psycopg2://postgres:{password}@{host}/{database}")

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class User(Base):
    __tablename__ = 'users'

    tg_id = Column(BIGINT, unique=True)
    organization_id = Column(BIGINT)
    phone = Column(String)
    user_pin = Column(BIGINT, primary_key=True)

Base.metadata.create_all(bind=engine)  # Create Table if not exist

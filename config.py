import os
from dotenv import load_dotenv


load_dotenv()
Token = os.getenv('TOKEN')
db_pass = os.getenv('db_pass')
db_name = os.getenv('db_name')
db_user = os.getenv('db_user')
host = os.getenv("host")

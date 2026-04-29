# import mysql.connector

# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="KidanFer22G@",
#     database="smart_task_db"
# )

# cursor = conn.cursor(dictionary=True)

# import os
# import mysql.connector
# from dotenv import load_dotenv

# load_dotenv()

# conn = mysql.connector.connect(
#     host=os.getenv("DB_HOST"),
#     port=int(os.getenv("DB_PORT", 3306)),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     database=os.getenv("DB_NAME"),
#     ssl_disabled=False
# )

# cursor = conn.cursor(dictionary=True)

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_disabled=False
    )
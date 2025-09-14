import sqlite3
from config import DB_PATH

def get_sqlit_conn():

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)

    return conn
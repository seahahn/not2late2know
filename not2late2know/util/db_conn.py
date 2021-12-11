import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PW')
database = os.getenv('DB_NAME')

# 데이터베이스 연결하는 함수
def db_conn():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()

    return connection, cursor

# 테이블에 데이터 저장하는 함수
def exec_insert(query):
    connection, cursor = db_conn()
    cursor.execute(query)
    connection.commit()
    connection.close()

# 테이블의 데이터 조회하는 함수
def exec_select(query):
    connection, cursor = db_conn()
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results
'''
온실 가스 데이터 저장하는 스케줄러 함수 구현

이산화탄소(일 단위) : 1시간(매 시간의 3분)마다 전일 데이터 존재 여부 확인 후 있으면 저장
메탄(월 단위) : 매일 0시 5분에 전월 데이터 존재 여부 확인 후 있으면 저장 (데이터베이스 연결 중첩 방지)
아산화질소(월 단위) : 매일 0시 10분에 전월 데이터 존재 여부 확인 후 있으면 저장 (데이터베이스 연결 중첩 방지)
'''
from db_conn import db_conn, exec_insert, exec_select
import time
from datetime import date, timedelta
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# 스케줄러 선언
scheduler = BackgroundScheduler(timezone=utc)

# 이산화탄소 데이터 스케줄러 함수
# 1시간(매 시간의 3분)마다 실행
# @scheduler.scheduled_job('interval', seconds=5)
@scheduler.scheduled_job('cron', minute='3')
def co2_insert():
    # 요청 URL 전송 및 데이터 불러오기
    response = requests.get(url='https://global-warming.org/api/co2-api').json()['co2'][-1]

    year = response['year']
    month = response['month']
    day = response['day']
    co2 = response['trend']
    row = (year, month, day, co2) # 삽입할 데이터 행 만들기

    insert_query = "INSERT INTO co2_test (year, month, day, co2) VALUES {};".format(row)
    select_query = "SELECT * FROM co2_test WHERE year = {} AND month = {} AND day = {}".format(row[0], row[1], row[2])

    # 동일한 년, 월의 데이터가 있는지 확인
    result = exec_select(select_query)

    # 데이터 없으면 삽입문 전송
    if len(result) == 0:
        exec_insert(insert_query)

# 메탄 데이터 스케줄러 함수
# 매일 0시 5분에 실행
# @scheduler.scheduled_job('interval', seconds=5)
@scheduler.scheduled_job('cron', hour='0', minute='5')
def methane_insert():
    # 요청 URL 전송 및 데이터 불러오기
    response = requests.get(url='https://global-warming.org/api/methane-api').json()['methane'][-1]

    _date = response['date'].split('.')
    year = _date[0]
    month = _date[1]
    methane = response['trend']
    row = (year, month, methane) # 삽입할 데이터 행 만들기

    insert_query = "INSERT INTO methane (year, month, methane) VALUES {};".format(row)
    select_query = "SELECT * FROM methane WHERE year = {} AND month = {}".format(row[0], row[1])

    # 동일한 년, 월의 데이터가 있는지 확인
    result = exec_select(select_query)

    # 데이터 없으면 삽입문 전송
    if len(result) == 0:
        exec_insert(insert_query)

# 아산화질소 데이터 스케줄러 함수
# 매일 0시 10분에 실행
# @scheduler.scheduled_job('interval', seconds=5)
@scheduler.scheduled_job('cron', hour='0', minute='10')
def nitrous_insert():
    # 요청 URL 전송 및 데이터 불러오기
    response = requests.get(url='https://global-warming.org/api/nitrous-oxide-api').json()['nitrous'][-1]

    _date = response['date'].split('.')
    year = _date[0]
    month = _date[1]
    nitrous = response['trend']
    row = (year, month, nitrous) # 삽입할 데이터 행 만들기

    insert_query = "INSERT INTO nitrous_test (year, month, nitrous) VALUES {};".format(row)
    select_query = "SELECT * FROM nitrous_test WHERE year = {} AND month = {}".format(row[0], row[1])

    # 동일한 년, 월의 데이터가 있는지 확인
    result = exec_select(select_query)

    # 데이터 없으면 삽입문 전송
    if len(result) == 0:
        exec_insert(insert_query)

# 스케줄러 수행 시작
scheduler.start()

# 스케줄러 지속 실행을 위한 반복문 수행
while True:
    time.sleep(5)
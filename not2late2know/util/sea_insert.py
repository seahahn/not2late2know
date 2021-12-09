'''
북극 해빙 데이터 저장하는 스케줄러 함수 구현

북극 해빙 면적(년 단위) : 매일 1시에 전년 데이터 존재 여부 확인 후 있으면 저장
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

scheduler = BackgroundScheduler(timezone=utc)

# 북극 해빙 면적 데이터 스케줄러 함수
# 매일 1시에 실행
# @scheduler.scheduled_job('interval', seconds=5)
@scheduler.scheduled_job('cron', hour='1')
def sea_ice_insert():
    # 요청 URL 전송 및 데이터 불러오기
    response = requests.get(url='https://global-warming.org/api/arctic-api').json()['result'][-1]

    year = response['year']
    extent = response['extent']
    area = response['area']
    row = (year, extent, area) # 삽입할 데이터 행 만들기

    insert_query = "INSERT INTO sea_ice_test (year, extent, area) VALUES {};".format(row)
    select_query = "SELECT * FROM sea_ice_test WHERE year = {}".format(row[0])

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
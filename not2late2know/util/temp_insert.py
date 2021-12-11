'''
1954년부터 현재까지의 서울 기온 데이터와
세계 평균 기온 데이터 저장하는 스케줄러 함수 구현

서울 기온 데이터는 매일 오전 11시 30분에 전일 기온 데이터를 받아온 후 DB에 저장.
세계 평균 기온 데이터는 매일 0시에 전월 데이터 존재 여부 확인 후 있으면 저장.
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

# 공공데이터포털 get 요청 URL을 문자열로 변환. 안 하면 특수문자 유니코드로 인식해서 API 키 안 먹힘.
def get_request_query(url, operation, params, serviceKey):
    import urllib.parse as urlparse
    params = urlparse.urlencode(params)
    request_query = url + '/' + operation + '?' + 'serviceKey' '=' + serviceKey + '&' + params
    return request_query

# 스케줄러 선언
scheduler = BackgroundScheduler(timezone=utc)

# 서울 기온 데이터 스케줄러 함수
# 매일 오전 11시 30분에 실행
@scheduler.scheduled_job('interval', seconds=5)
# @scheduler.scheduled_job('cron', hour='11', minute='10')
def temp_insert():
    # 요청 URL과 오퍼레이션
    URL = 'http://apis.data.go.kr/1360000/AsosDalyInfoService'
    OPERATION = 'getWthrDataList'
    SERVICEKEY = os.getenv('TEMP_API_KEY')
    PARAMS = {'dataType': 'JSON',
                'dataCd': 'ASOS',
                'dateCd': 'DAY',
                'startDt': str(date.today()-timedelta(days = 3)).replace("-", ""), # 3일 전 날짜부터 어제 날짜까지의 기온 데이터 조회
                'endDt': str(date.today()-timedelta(days = 1)).replace("-", ""),
                'stnIds': 108}
    request_query = get_request_query(URL, OPERATION, PARAMS, SERVICEKEY)

    try:
        # 요청 URL 전송 및 데이터 불러오기
        responses = requests.get(url=request_query).json()['response']['body']['items']['item']

        for i, response in enumerate(responses):
            _date = response['tm'].split("-") # 년, 월, 일로 나누기

            # 삽입할 데이터 행 만들기
            row = (_date[0], _date[1], _date[2], response['avgTa'], response['minTa'], response['maxTa'])

            insert_query = "INSERT INTO temp (year, month, day, avgtmp, mintmp, maxtmp) VALUES {};".format(row)
            select_query = "SELECT * FROM temp WHERE year = {} AND month = {} AND day = {}".format(row[0], row[1], row[2])

            # 동일한 년, 월의 데이터가 있는지 확인
            result = exec_select(select_query)

            if len(result) == 0:
                exec_insert(insert_query)
                print("inserting executed global_temp_insert")

        print("executed temp_insert")
    except Exception as e:
        print(e)

# 세계 평균 기온 데이터 스케줄러 함수
# 매일 0시에 실행
@scheduler.scheduled_job('interval', seconds=5)
# @scheduler.scheduled_job('cron', hour='0')
def global_temp_insert():
    # 요청 URL 전송 및 데이터 불러오기
    response = requests.get(url='https://global-warming.org/api/temperature-api').json()['result'][-1]

    # 월 자리의 문자를 해당하는 월 숫자로 변환
    month_map = {'04':1, '13':2, '21':3, '29':4, '38':5, '46':6, '54':7, '63':8, '71':9, '79':10, '88':11, '96':12}

    _date = response['time'].split(".") # 년 그리고 월 자리의 문자로 나누기
    row = (_date[0], month_map[_date[1]], response['station']) # 삽입할 데이터 행 만들기

    insert_query = "INSERT INTO global_temp (year, month, tmp) VALUES {};".format(row)
    select_query = "SELECT * FROM global_temp WHERE year = {} AND month = {}".format(row[0], row[1])

    # 동일한 년, 월의 데이터가 있는지 확인
    result = exec_select(select_query)

    # 데이터 없으면 삽입문 전송
    if len(result) == 0:
        exec_insert(insert_query)
        print("inserting executed global_temp_insert")

    print("executed global_temp_insert")

# 스케줄러 수행 시작
scheduler.start()

# 스케줄러 지속 실행을 위한 반복문 수행
while True:
    time.sleep(5)
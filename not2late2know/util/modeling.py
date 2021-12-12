import warnings, logging, os
from joblib import dump, load
from .db_conn import exec_select
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

warnings.filterwarnings(action='ignore')

BASE_DIR = os.path.dirname(__file__)

gbtemp_query = "SELECT * FROM global_temp"
gbtemp_columns = ['year', 'month', 'tmp']
co2_query = "SELECT * FROM co2"
co2_columns=['year', 'month', 'day', 'co2']
methane_query = "SELECT * FROM methane"
methane_columns=['year', 'month', 'methane']
nitrous_query = "SELECT * FROM nitrous"
nitrous_columns=['year', 'month', 'nitrous']

querys = [gbtemp_query, co2_query, methane_query, nitrous_query]
column_sets = [gbtemp_columns, co2_columns, methane_columns, nitrous_columns]
targets = [gbtemp_columns[-1], co2_columns[-1], methane_columns[-1], nitrous_columns[-1]]
model_save_names = ['model_gbtemp', 'model_co2', 'model_methane', 'model_nitrous']

# 데이터셋을 데이터프레임 형태로 변환하는 함수
def query(query, columns):
    result = exec_select(query)
    df = pd.DataFrame(result, columns=columns)

    return df

# 모델 학습을 위한 함수
def processing(df, target):
    # 특성과 타겟 분리하기
    target = target
    features = df.drop(columns=target).columns

    X = df[features]
    y = df[target]

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=2)

    pipe = make_pipeline(
        PolynomialFeatures(degree=2, include_bias=True),
        LinearRegression()
    )
    pipe.fit(X_train, y_train)

    return pipe

# 모델 학습 후 모델 객체 저장하는 스케줄링 함수
# 매일 2시에 진행(머신 러닝 모델 학습 대상 데이터 중 북극 해빙 데이터 수집이 1시에 진행됨)
scheduler = BackgroundScheduler(timezone=utc)
@scheduler.scheduled_job('interval', seconds=30)
# @scheduler.scheduled_job('cron', hour='2')
def model_fit():
    for q, col, target, model_name in zip(querys, column_sets, targets, model_save_names):
        model = processing(query(q, col), target)
        # path = F"{BASE_DIR}/ml_models/{model_name}.joblib"
        path = os.path.join(BASE_DIR, f"ml_models/{model_name}.joblib")
        dump(model, path)
        log_message = "modeling executed:{}".format(datetime.now())
        print(log_message)
        logging.debug(log_message)

# model_gbtemp = processing(query(gbtemp_query, gbtemp_columns), gbtemp_columns[-1])
# model_co2 = processing(query(co2_query, co2_columns), co2_columns[-1])
# model_methane = processing(query(methane_query, methane_columns), methane_columns[-1])
# model_nitrous = processing(query(nitrous_query, nitrous_columns), nitrous_columns[-1])

# models = [model_gbtemp, model_co2, model_methane, model_nitrous]
# model_save_names = ['model_gbtemp', 'model_co2', 'model_methane', 'model_nitrous']

# # 모델 저장하기
# for model, model_save_name in zip(models, model_save_names):
# path = F"not2late2know/util/ml_models/{model_save_name}.joblib"
# dump(model, path)

# 모델 불러오기
# for model, model_save_name in zip(models, model_save_names):
#   load_path = F"not2late2know/util/ml_models/{model_save_name}.joblib"
#   model = load(load_path)

# load_path = F"not2late2know/util/ml_models/model_gbtemp.joblib"
# model = load(load_path)

# print(model.predict([[2020, 1]]))
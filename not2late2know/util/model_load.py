import warnings
from joblib import dump, load
from .db_conn import exec_select
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

warnings.filterwarnings(action='ignore')

gbtemp_query = "SELECT * FROM global_temp"
gbtemp_columns = ['year', 'month', 'tmp']
co2_query = "SELECT * FROM co2"
co2_columns=['year', 'month', 'day', 'co2']
methane_query = "SELECT * FROM methane"
methane_columns=['year', 'month', 'methane']
nitrous_query = "SELECT * FROM nitrous"
nitrous_columns=['year', 'month', 'nitrous']

def query(query, columns):
    result = exec_select(query)
    df = pd.DataFrame(result, columns=columns)

    return df

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

# model_gbtemp = processing(query(gbtemp_query, gbtemp_columns), gbtemp_columns[-1])
# model_co2 = processing(query(co2_query, co2_columns), co2_columns[-1])
# model_methane = processing(query(methane_query, methane_columns), methane_columns[-1])
# model_nitrous = processing(query(nitrous_query, nitrous_columns), nitrous_columns[-1])

# models = [model_gbtemp, model_co2, model_methane, model_nitrous]
# model_save_names = ['model_gbtemp', 'model_co2', 'model_methane', 'model_nitrous']

# 모델 저장하기
# for model, model_save_name in zip(models, model_save_names):
#   path = F"not2late2know/util/ml_models/{model_save_name}.joblib"
#   dump(model, path)

# 모델 불러오기
# for model, model_save_name in zip(models, model_save_names):
#   load_path = F"not2late2know/util/ml_models/{model_save_name}.joblib"
#   model = load(load_path)
  
# load_path = F"not2late2know/util/ml_models/model_gbtemp.joblib"
# model = load(load_path)

# print(model.predict([[2020, 1]]))
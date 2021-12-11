from flask import Blueprint, render_template
import pandas as pd
from datetime import date
from util.db_conn import db_conn, exec_insert, exec_select
from util.model_load import gbtemp_query, gbtemp_columns, co2_query, co2_columns, methane_query, methane_columns, nitrous_query, nitrous_columns

bp = Blueprint('api', __name__, template_folder='templates')

months = [mon for mon in range(1,13)]
this_year = date.today().year

@bp.route('/api/global-temp/', defaults={'year':None, 'month':None}, methods=['GET'])
@bp.route('/api/global-temp/<int:year>', defaults={'month':None}, methods=['GET'])
@bp.route('/api/global-temp/<int:year>/<int:month>', methods=['GET'])
def global_temp(year, month):
    result = exec_select(gbtemp_query)
    df = pd.DataFrame(result, columns=gbtemp_columns)

    years = df.year.to_list()

    if year is None and month is None: # year와 month 모두 없을 경우 전체 데이터 보내기
        return df.to_json(orient = 'records'), 200

    elif month is None: # year만 있을 경우 year에 해당하는 데이터 보내기
        if year not in years: # year가 DB에 존재하지 않는 값일 경우 에러 반환
            return 'We are sorry. Year {} doesn\'t exist in this database. Please enter between {} and {}.'.format(year, years[0], years[-1]), 404

        query = "SELECT * FROM global_temp WHERE year = '{}'".format(year)
        result = exec_select(query)
        df = pd.DataFrame(result, columns=gbtemp_columns)
        return df.to_json(orient = 'records'), 200

    elif month not in months: # 월 숫자를 잘못 입력한 경우
        return '{} is not a valid month'.format(month), 404

    else: # year와 month 모두 있을 경우 year와 month에 해당하는 데이터 보내기
        query = "SELECT * FROM global_temp WHERE year = '{}' AND month = '{}'".format(year, month)
        result = exec_select(query)
        df = pd.DataFrame(result, columns=gbtemp_columns)

        if df.empty: # 데이터가 없을 경우 에러 반환
            return 'We are sorry. Month {} doesn\'t exist in year {} in this database.'.format(month, year), 404

        return df.to_json(orient = 'records'), 200

@bp.route('/api/co2/', defaults={'year':None, 'month':None, 'day':None}, methods=['GET'])
@bp.route('/api/co2/<int:year>', defaults={'month':None, 'day':None}, methods=['GET'])
@bp.route('/api/co2/<int:year>/<int:month>', defaults={'day':None}, methods=['GET'])
@bp.route('/api/co2/<int:year>/<int:month>/<int:day>', methods=['GET'])
def co2(year, month, day):
    co2 = exec_select(co2_query)
    df = pd.DataFrame(co2, columns=co2_columns)

    years = df.year.to_list()

    if year is None and month is None and day is None: # year, month, day 모두 없을 경우 전체 데이터 보내기
        return df.to_json(orient = 'records'), 200

    elif month is None and day is None: # year만 있을 경우 year에 해당하는 데이터 보내기
        if year not in years: # year가 DB에 존재하지 않는 값일 경우 에러 반환
            return 'We are sorry. Year {} doesn\'t exist in this database. Please enter between {} and {}.'.format(year, years[0], years[-1]), 404

        query = "SELECT * FROM co2 WHERE year = '{}'".format(year)
        result = exec_select(query)
        df = pd.DataFrame(result, columns=co2_columns)
        return df.to_json(orient = 'records'), 200

    elif year is not None and month is not None: # year, month만 있을 경우 year와 month에 해당하는 데이터 보내기
        if month not in months: # 월 숫자를 잘못 입력한 경우
            return '{} is not a valid month'.format(month), 404

        query = "SELECT * FROM co2 WHERE year = '{}' AND month = '{}'".format(year, month)
        result = exec_select(query)
        df = pd.DataFrame(result, columns=co2_columns)

        if df.empty: # 데이터가 없을 경우 에러 반환
            return 'We are sorry. Month {} doesn\'t exist in year {} in this database.'.format(month, year), 404

        return df.to_json(orient = 'records'), 200

    else: # year, month, day 모두 있을 경우 조건에 해당하는 데이터 보내기
        query = "SELECT * FROM co2 WHERE year = '{}' AND month = '{}' AND day = '{}'".format(year, month, day)
        result = exec_select(query)
        df = pd.DataFrame(result, columns=co2_columns)

        if df.empty: # 데이터가 없을 경우 에러 반환
            return 'We are sorry. Day {} doesn\'t exist in {}-{} in this database.'.format(day, year, month), 404

        return df.to_json(orient = 'records'), 200

@bp.route('/api/methane/', defaults={'year':None, 'month':None}, methods=['GET'])
@bp.route('/api/methane/<int:year>', defaults={'month':None}, methods=['GET'])
@bp.route('/api/methane/<int:year>/<int:month>', methods=['GET'])
def methane(year, month):
    result = exec_select(methane_query)
    df = pd.DataFrame(result, columns=methane_columns)

    years = df.year.to_list()

    if year is None and month is None: # year와 month 모두 없을 경우 전체 데이터 보내기
        return df.to_json(orient = 'records'), 200

    elif month is None: # year만 있을 경우 year에 해당하는 데이터 보내기
        if year not in years: # year가 DB에 존재하지 않는 값일 경우 에러 반환
            return 'We are sorry. Year {} doesn\'t exist in this database. Please enter between {} and {}.'.format(year, years[0], years[-1]), 404

        query = "SELECT * FROM methane WHERE year = '{}'".format(year)
        result = exec_select(query)
        df = pd.DataFrame(result, columns=methane_columns)
        return df.to_json(orient = 'records'), 200

    elif month not in months: # 월 숫자를 잘못 입력한 경우
        return '{} is not a valid month'.format(month), 404

    else: # year와 month 모두 있을 경우 year와 month에 해당하는 데이터 보내기
        query = "SELECT * FROM methane WHERE year = '{}' AND month = '{}'".format(year, month)
        result = exec_select(query)
        df = pd.DataFrame(result, columns=methane_columns)

        if df.empty: # 데이터가 없을 경우 에러 반환
            return 'We are sorry. Month {} doesn\'t exist in year {} in this database.'.format(month, year), 404

        return df.to_json(orient = 'records'), 200

@bp.route('/api/nitrous/', defaults={'year':None, 'month':None}, methods=['GET'])
@bp.route('/api/nitrous/<int:year>', defaults={'month':None}, methods=['GET'])
@bp.route('/api/nitrous/<int:year>/<int:month>', methods=['GET'])
def nitrous(year, month):
    result = exec_select(methane_query)
    df = pd.DataFrame(result, columns=nitrous_columns)

    years = df.year.to_list()

    if year is None and month is None: # year와 month 모두 없을 경우 전체 데이터 보내기
        return df.to_json(orient = 'records'), 200

    elif month is None: # year만 있을 경우 year에 해당하는 데이터 보내기
        if year not in years: # year가 DB에 존재하지 않는 값일 경우 에러 반환
            return 'We are sorry. Year {} doesn\'t exist in this database. Please enter between {} and {}.'.format(year, years[0], years[-1]), 404

        query = "SELECT * FROM nitrous WHERE year = '{}'".format(year)
        result = exec_select(query)
        df = pd.DataFrame(result, columns=nitrous_columns)
        return df.to_json(orient = 'records'), 200

    elif month not in months: # 월 숫자를 잘못 입력한 경우
        return '{} is not a valid month'.format(month), 404

    else: # year와 month 모두 있을 경우 year와 month에 해당하는 데이터 보내기
        query = "SELECT * FROM nitrous WHERE year = '{}' AND month = '{}'".format(year, month)
        result = exec_select(query)
        df = pd.DataFrame(result, columns=nitrous_columns)

        if df.empty: # 데이터가 없을 경우 에러 반환
            return 'We are sorry. Month {} doesn\'t exist in year {} in this database.'.format(month, year), 404

        return df.to_json(orient = 'records'), 200

@bp.route('/api/sea-ice/', defaults={'year':None}, methods=['GET'])
@bp.route('/api/sea-ice/<int:year>', methods=['GET'])
def sea_ice(year):
    query = "SELECT * FROM sea_ice"
    sea_ice_columns = ['year', 'extent', 'area']
    result = exec_select(query)
    df = pd.DataFrame(result, columns=sea_ice_columns)

    years = df.year.to_list()

    if year is None:
        return df.to_json(orient = 'records'), 200
    elif year not in years:
        return 'We are sorry. Year {} doesn\'t exist in this database. Please enter between {} and {}.'.format(year, years[0], years[-1]), 404
    else:
        query = "SELECT * FROM sea_ice WHERE year = '{}'".format(year)
        result = exec_select(query)
        df = pd.DataFrame(result, columns=sea_ice_columns)

        return df.to_json(orient = 'records'), 200

@bp.route('/api/sea-level/', defaults={'year':None}, methods=['GET'])
@bp.route('/api/sea-level/<int:year>', methods=['GET'])
def sea_level(year):
    query = "SELECT * FROM sea_level"
    sea_level_columns = ['year', 'level']
    result = exec_select(query)
    df = pd.DataFrame(result, columns=sea_level_columns)

    years = df.year.to_list()

    if year is None:
        return df.to_json(orient = 'records'), 200
    elif year not in years:
        return 'We are sorry. Year {} doesn\'t exist in this database. Please enter between {} and {}.'.format(year, years[0], years[-1]), 404
    else:
        query = "SELECT * FROM sea_level WHERE year = '{}'".format(year)
        result = exec_select(query)
        df = pd.DataFrame(result, columns=sea_level_columns)

        return df.to_json(orient = 'records'), 200
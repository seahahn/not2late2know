from flask import Blueprint, render_template
import pandas as pd
from util.db_conn import db_conn, exec_insert, exec_select
from util.modeling import gbtemp_query, gbtemp_columns, co2_query, co2_columns, methane_query, methane_columns, nitrous_query, nitrous_columns

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/main')
def main():
    return render_template('index.html')

def return_gbtemp_json():
    result = exec_select(gbtemp_query)
    df = pd.DataFrame(result, columns=gbtemp_columns)
    df['time'] = df['year'].astype(str) + '-' + df['month'].astype(str)
    return df.to_json(orient = 'columns')
def return_ghgas_json():
    co2 = exec_select(co2_query)
    methane = exec_select(methane_query)
    nitrous = exec_select(nitrous_query)
    df_co2 = pd.DataFrame(co2, columns=co2_columns)
    df_methane = pd.DataFrame(methane, columns=methane_columns)
    df_nitrous = pd.DataFrame(nitrous, columns=nitrous_columns)

    df_co2['time'] = df_co2['year'].astype(str) + '-' + df_co2['month'].astype(str) + '-' + df_co2['day'].astype(str)
    df_methane['time'] = df_methane['year'].astype(str) + '-' + df_methane['month'].astype(str)
    df_nitrous['time'] = df_nitrous['year'].astype(str) + '-' + df_nitrous['month'].astype(str)
    return df_co2.to_json(orient = 'columns'), df_methane.to_json(orient = 'columns'), df_nitrous.to_json(orient = 'columns')
def return_seaice_json():
    query = "SELECT * FROM sea_ice"
    result = exec_select(query)
    df = pd.DataFrame(result, columns=['year', 'extent', 'area'])
    return df.to_json(orient = 'columns')
def return_sealevel_json():
    query = "SELECT * FROM sea_level"
    result = exec_select(query)
    df = pd.DataFrame(result, columns=['year', 'level'])
    return df.to_json(orient = 'columns')

@bp.route('/global-temp')
def global_temp():
    return render_template('global-temp.html', gbtemp=return_gbtemp_json())

@bp.route('/greenhouse-gas')
def greenhouse_gas():
    df_co2, df_methane, df_nitrous = return_ghgas_json()
    return render_template('greenhouse-gas.html', co2=df_co2, methane=df_methane, nitrous=df_nitrous)

@bp.route('/sea-ice')
def sea_ice():
    return render_template('sea-ice.html', sea_ice=return_seaice_json())

@bp.route('/sea-level')
def sea_level():
    return render_template('sea-level.html', sea_level=return_sealevel_json())

@bp.route('/summary')
def summary():
    df_co2, df_methane, df_nitrous = return_ghgas_json()
    return render_template('summary.html', gbtemp=return_gbtemp_json(), co2=df_co2, methane=df_methane, nitrous=df_nitrous, sea_ice=return_seaice_json(), sea_level=return_sealevel_json())
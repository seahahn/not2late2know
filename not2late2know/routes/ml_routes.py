from flask import Blueprint, request
from joblib import dump, load

bp = Blueprint('ml', __name__, template_folder='templates')

@bp.route('/ml/global-temp/', methods=['GET'])
def global_temp():
    year = request.args.get('year')
    month = request.args.get('month')

    load_path = F"not2late2know/util/ml_models/model_gbtemp.joblib"
    model = load(load_path)
    result = round(model.predict([[year, month]])[0], 2)

    return str(result)

@bp.route('/ml/co2/', methods=['GET'])
def co2():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')

    load_path = F"not2late2know/util/ml_models/model_co2.joblib"
    model = load(load_path)
    result = round(model.predict([[year, month, day]])[0], 2)

    return str(result)

@bp.route('/ml/methane/', methods=['GET'])
def methane():
    year = request.args.get('year')
    month = request.args.get('month')

    load_path = F"not2late2know/util/ml_models/model_methane.joblib"
    model = load(load_path)
    result = round(model.predict([[year, month]])[0], 2)

    return str(result)

@bp.route('/ml/nitrous/', methods=['GET'])
def nitrous():
    year = request.args.get('year')
    month = request.args.get('month')

    load_path = F"not2late2know/util/ml_models/model_nitrous.joblib"
    model = load(load_path)
    result = round(model.predict([[year, month]])[0], 2)

    return str(result)
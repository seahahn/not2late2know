from flask import Blueprint, render_template

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/main')
def main():
    return render_template('index.html')

@bp.route('/arctic')
def arctic():
    return render_template('arctic.html')

@bp.route('/elements')
def elements():
    return render_template('elements.html')

@bp.route('/generic')
def generic():
    return render_template('generic.html')

@bp.route('/landing')
def landing():
    return render_template('landing.html')
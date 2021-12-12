from flask import Flask
import sys, os, logging

def create_app():
    app = Flask(__name__)
    logging_setting() # 로그 기록 남기기 세팅

    # 웹페이지 라우트 설정
    from routes import main_routes
    app.register_blueprint(main_routes.bp)
    from routes import api_routes
    app.register_blueprint(api_routes.bp)
    from routes import ml_routes
    app.register_blueprint(ml_routes.bp)

    # DB에 데이터 저장 수행하는 스케줄러 설정
    from util import temp_insert
    temp_scheduler = temp_insert.scheduler
    from util import gas_insert
    gas_scheduler = gas_insert.scheduler
    from util import sea_insert
    sea_scheduler = sea_insert.scheduler
    # 모델 학습 및 모델 객체 저장하는 스케줄러 설정
    from util import modeling
    model_scheduler = modeling.scheduler

    # 스케줄러 시작
    temp_scheduler.start()
    gas_scheduler.start()
    sea_scheduler.start()
    model_scheduler.start()

    return app

def logging_setting():
    import logging
    from logging.handlers import RotatingFileHandler
    from logging import Formatter

    app.config['LOGGING_LEVEL'] = logging.INFO
    app.config['LOGGING_FORMAT'] = '%(asctime)s %(levelname)s: %(message)s in %(filename)s:%(lineno)d]'
    app.config['LOGGING_LOCATION'] = 'not2late2know/logs/'
    app.config['LOGGING_FILENAME'] = 'log_record.log'
    app.config['LOGGING_MAX_BYTES'] = 100000
    app.config['LOGGING_BACKUP_COUNT'] = 1000

    # logging
    if not app.debug:
        log_dir = os.path.join(app.config['HOME_DIR'], app.config['LOGGING_LOCATION'])
        file_handler = RotatingFileHandler(log_dir + app.config['LOGGING_FILENAME'], maxBytes=app.config['LOGGING_MAX_BYTES'], backupCount=app.config['LOGGING_BACKUP_COUNT'])
        file_handler.setFormatter(Formatter(app.config['LOGGING_FORMAT']))
        file_handler.setLevel(app.config['LOGGING_LEVEL'])
        app.logger.addHandler(file_handler)
        app.logger.info("logging start")


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
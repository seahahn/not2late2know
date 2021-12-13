from flask import Flask

def create_app():
    app = Flask(__name__)

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

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)
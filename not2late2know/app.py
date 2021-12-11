from flask import Flask

def create_app():
    app = Flask(__name__)

    from routes import main_routes
    app.register_blueprint(main_routes.bp)
    from routes import api_routes
    app.register_blueprint(api_routes.bp)
    from routes import ml_routes
    app.register_blueprint(ml_routes.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
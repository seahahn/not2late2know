from flask import Flask

def create_app():
    app = Flask(__name__)

    from dnd_app.routes import main_routes
    app.register_blueprint(main_routes.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
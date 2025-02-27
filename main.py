import os
from flask import Flask
import atexit

from routes.gameroutes import game_routes
from routes.adminroutes import admin_routes

from utils.browserHelper import open_browser, close_browser

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    app.register_blueprint(game_routes)
    app.register_blueprint(admin_routes)

    env = os.getenv("ENV", "pi")
    url = "http://127.0.0.1:5000/game/"
    open_browser(env, url)
    atexit.register(lambda: close_browser(env))

    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5000)
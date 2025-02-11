import os
from flask import Flask

from routes.gameroutes import game_routes
from routes.adminroutes import admin_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

app.register_blueprint(game_routes)
app.register_blueprint(admin_routes)

if __name__ == '__main__':
    app.run()
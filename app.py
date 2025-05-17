from flask import Flask, redirect, request
from extensions import db, babel
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BABEL_DEFAULT_LOCALE'] = 'it'

db.init_app(app)
babel.init_app(app)

from blueprints.auth import auth_bp
from blueprints.games import games_bp
from blueprints.admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(games_bp)
app.register_blueprint(admin_bp)

@babel.localeselector
def get_locale():
    return request.args.get('lang') or 'it'

@app.route("/")
def home_redirect():
    return redirect("/auth/login")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

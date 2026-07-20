from flask import Flask
from flask_cors import CORS
from routes.auth import auth
from config import Config
from database import db
from flask_jwt_extended import JWTManager
from utils.email_service import mail
from routes.user import user
from routes.linkedin import linkedin
from routes.pages import pages
from routes.posts import posts
from extensions import scheduler
import extensions
import os

app = Flask(__name__)

app.config.from_object(Config)

extensions.flask_app = app

scheduler.init_app(app)

scheduler.start()
print("APScheduler started successfully")
    
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(linkedin, url_prefix="/linkedin")
app.register_blueprint(pages)
app.register_blueprint(posts, url_prefix="/posts")

mail.init_app(app)

app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False      # True in production with HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)

db.init_app(app)

CORS(
    app,
    supports_credentials=True
)

with app.app_context():
    db.create_all()

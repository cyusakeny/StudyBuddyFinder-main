from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
secret_key = os.getenv('SECRET_KEY')

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
s = URLSafeTimedSerializer(secret_key)

def create_app():
    app = Flask(__name__)
    app.config.from_object('study.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    from study.db_models import User
    from .routes import register_routes

    @login_manager.user_loader
    def load_user(username):
        return User.query.get(username)

    with app.app_context():
        db.create_all()

    register_routes(app)
    
    return app

def generate_confirmation_token(email):
    return s.dumps(email, salt='email-confirmation-salt')

def confirm_token(token, expiration=3600):
    try:
        email = s.loads(token, salt='email-confirmation-salt', max_age=expiration)
    except:
        return False
    return email

from study.google_apis import send_email  # Import the new send_email function

def send_confirmation_email(user_email):
    token = generate_confirmation_token(user_email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('email/activate.html', confirm_url=confirm_url)
    send_email(user_email, 'Please confirm your email', html)

from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager
from os import path, getenv
from dotenv import load_dotenv
from flask_mail import Mail


db = SQLAlchemy()
mail_sender = Mail()
DB_NAME = 'admin.db'
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv("SQLALCHEMY_DATABASE_URI")
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = getenv("EMAIL_USER")
    app.config['MAIL_PASSWORD'] = getenv('EMAIL_PASSWORD')
    app.config['MAIL_USE_SSL'] = True
    db.init_app(app)
    mail_sender.init_app(app)
    from .views import views
    from .auth import auth


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/admin/')
    
    from .models import Admin, Blog

    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Admin.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print("created Database!")
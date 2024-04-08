from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from .config import DevConfig
from .extension import db, bcrypt
from .auth import auth_bp
from .base import base_bp
from .models import Employee, Post, Opportunity, Comments
import os

def construct_app(test_config=None):
    # Load environment variables from .env file
    load_dotenv()
    
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_mapping(
        SECRET_KEY= os.getenv('SECRET_KEY', 'development'),
        DATABASE=os.path.join(application.instance_path, 'opportunity_tracker.sqlite'),
        LOGIN_VIEW='auth.login'
        #RECAPTCHA_PUBLIC_KEY=os.getenv('RECAPTCHA_PUBLIC_KEY'),
        #RECAPTCHA_PRIVATE_KEY=os.getenv('RECAPTCHA_PRIVATE_KEY')
    )
    
     
    login_manager = LoginManager()
    login_manager.init_app(application)
    
 
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = "danger"
    
    @login_manager.user_loader
    def load_user(user_id):
        return Employee.query.get(int(user_id))

    if test_config is None:
        application.config.from_object(DevConfig)  
    else:
        application.config.from_mapping(test_config)

    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass

    # Initialse db and bcrypt with the application
    db.init_app(application)
    bcrypt.init_app(application)

   
    migrate = Migrate(application, db)

    application.register_blueprint(auth_bp)
    application.register_blueprint(base_bp)

  

    return application
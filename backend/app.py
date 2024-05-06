from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_security import SQLAlchemyUserDatastore, Security
from werkzeug.security import generate_password_hash

def create_app():
    from application.models import db, User, Role, UserRoles, Creator
    app = Flask(__name__)
    CORS(app) 

    app.config["SECRET_KEY"] = "iiytghhgh"
    app.config["SECURITY_PASSWORD_SALT"] = "dfswert"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///music_app.db"
    app.config['UPLOAD_FOLDER'] = 'application/static/songs'
    # app.config['ALLOWED_EXTENSIONS'] = {'mp3'}
    app.config['SMTP_SERVER'] = 'localhost'
    app.config['SMTP_PORT'] = 1025
    app.config['SENDER_EMAIL'] = 'ARJITA@study.iitm.ac.in'
    app.config['SENDER_PASSWORD'] = ''
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL']='redis://localhost:6379/0'
    app.config['CACHE_DEFAULT_TIMEOUT']=30
    app.config['CACHE_KEY_PREFIX'] = "caching"

    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)
    from application.views import api, cache
    db.init_app(app)
    cache.init_app(app)
    
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

        if not Role.query.filter_by(name="admin").first():
            app.security.datastore.create_role(name="admin")
            app.security.datastore.create_role(name="user")
            app.security.datastore.create_role(name="creator")
            db.session.commit()

        admin_user = User.query.filter_by(email="admin@gmail.com").first()
        user = User.query.filter_by(email="abc@gmail.com").first()
        if not admin_user:
            admin_user = datastore.create_user(name="admin",email="admin@gmail.com",password=generate_password_hash("admin_password"))
            admin_role = Role.query.filter_by(name="admin").first()
            datastore.add_role_to_user(admin_user, admin_role)
            db.session.commit()

        if not user:
            user = datastore.create_user(name="abc", email="abc@gmail.com",password=generate_password_hash("abc"),)
            user_role = Role.query.filter_by(name="user").first()
            datastore.add_role_to_user(user, user_role)
            db.session.commit()

            creator_role = Role.query.filter_by(name="creator").first()
            datastore.add_role_to_user(user, creator_role)
            db.session.commit()

            creator = Creator(
                name="creator", bio="i love to create music", user=user)
            db.session.add(creator)
            db.session.commit()
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

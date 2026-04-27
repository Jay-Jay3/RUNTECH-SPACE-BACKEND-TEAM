from flask import Flask, request, jsonify
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# db = SQLAlchemy()
# migrate = Migrate()

# def create_app():
#     app = Flask(__name__)
#     swagger = Swagger(app)

#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db.init_app(app)
#     migrate.init_app(app, db)

#     from app.routes.auth import bp as authBP

#     app.register_blueprint(authBP)
#     return app

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'

    db.init_app(app)
    migrate = Migrate(app, db)

    from app.routes.auth import bp as authBP
    from app.routes.complaints import bp as complaintBP

    app.register_blueprint(authBP)
    app.register_blueprint(complaintBP)


    @app.route("/")
    def home():
        return "Campus Complaint & Feedback System is running!"

    return app
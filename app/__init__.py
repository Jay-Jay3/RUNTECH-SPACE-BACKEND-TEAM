from flask import Flask, request, jsonify
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api

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
migrate = Migrate() 


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'

    app.config["API_TITLE"]= "RUNTECH SPACE BACKEND"
    app.config["API_VERSION"]= "v1"
    app.config["OPENAPI_VERSION"]= "3.0.3"
    app.config["OPENAPI_URL_PREFIX"]= "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"]= "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"]= "https://unpkg.com/swagger-ui-dist@3.25.0/"


    # app.config['SWAGGER'] = {
    #     'title' : "RUNTECH SPACE BACKEND",
    #     'uiversion': "3",
    #     'specs_route' : '/docs'
    # }

    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)

    from app.routes.auth import bp as authBP
    from app.routes.complaints import bp as complaintBP
    from app.routes.home import bp as homeBP
    # from app.routes.user import bp as userBP
    # from app.routes.admin import bp as adminBP

    app.register_blueprint(authBP)
    app.register_blueprint(complaintBP)
    app.register_blueprint(homeBP)
    # app.register_blueprint(userBP)
    # app.register_blueprint(adminBP)


    return app
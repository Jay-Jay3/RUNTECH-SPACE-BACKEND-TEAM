from flask import Flask
from flask_migrate import Migrate
from model import db
from auth.routes import auth_bp
from complaints.routes import complaints_bp

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(complaints_bp)

    @app.route("/")
    def home():
        return "Campus Complaint & Feedback System is running!"

    return app

# Run directly
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


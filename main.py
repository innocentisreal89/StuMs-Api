from flask import Flask, jsonify
from flask_smorest import Api
from config.config import config_dict
from models.admin import AdminModel
from models.student import Student
from models.course import Course
from models.registered_course import RegisteredCourse
from db import db
from blocklist import BLOCKLIST
from auth.views import blp as AdminBlueprint
from resources.student import blp as StudentBlueprint
from resources.course import blp as CourseBlueprint
from flask_migrate import Migrate 

from flask_jwt_extended import JWTManager




#this function create the app
def create_app(config=config_dict['dev']):

    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    api = Api(app)


    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The Token has Expired.", "error": "token_expired"}), 401
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({
                "description": "Signature verification failed.",
                "error": "invalid token"
            }), 401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({
                "description": "Request does not contain an access token.",
                "error": "authorization_required"
            }), 401
        )


    #   Register the blueprints
    api.register_blueprint(AdminBlueprint)
    api.register_blueprint(StudentBlueprint)
    api.register_blueprint(CourseBlueprint)
    
    



    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'User':AdminModel,
            'Student':Student,
            'Course':Course,
            'StudentCourse': RegisteredCourse,
        }
    

    
    return app

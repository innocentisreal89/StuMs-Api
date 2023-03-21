from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from models.admin import AdminModel,check_last_email_char
from models.student import Student
from db import db
from datetime import timedelta
from schemas import PlainAdminSchema,AdminSignUpSchema,LoginSchema
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity,get_jwt
from blocklist import BLOCKLIST

blp = Blueprint('Admins', 'admins', description='Operation on Users')

#Register an Admin
@blp.route('/register-admin')
class AdminRegister(MethodView):
    @blp.arguments(AdminSignUpSchema)
    @blp.response(201, PlainAdminSchema)
    def post(self, admin_data):

        if check_last_email_char(admin_data["email"].lower()) != 'ui.edu.ng':
            abort(409, message="Invalid Email Address.")
        

        if AdminModel.query.filter(AdminModel.email == admin_data["email"].lower()).first():
            abort(409, message="A user with this email already exist.")

        if len(admin_data['password']) < 8 or  len(admin_data['password']) > 12:
            abort(409, message="Password must be within the range of 8 - 12 characters.")
        
        admin = AdminModel(
            firstName = admin_data['firstName'].lower(),
            lastName = admin_data['lastName'].lower(),
            email = admin_data['email'].lower(),
            password = pbkdf2_sha256.hash(admin_data["password"])
        )

        admin.save()

        return admin
    
#Login Function
@blp.route('/login')
class Login(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, user_data):

        if user_data['user_id'].startswith('ADMIN-UI'):
            user = AdminModel.query.filter(
            AdminModel.staff_id == user_data["user_id"]).first()

            if user and pbkdf2_sha256.verify(user_data["password"], user.password):
                access_token = create_access_token(identity=user.staff_id, fresh=True)
                refresh_token = create_refresh_token(identity=user.staff_id)

                return {"access_token": access_token, "refresh_token": refresh_token}

        elif user_data['user_id'].startswith('20'):
            student = Student.query.filter(
            Student.matric_no == user_data["user_id"]).first()

            if student and pbkdf2_sha256.verify(user_data["password"], student.password):
                access_token = create_access_token(identity=student.matric_no, fresh=True)
                refresh_token = create_refresh_token(identity=student.matric_no)
                return {"access_token": access_token, "refresh_token": refresh_token}
            
        else:
            abort(401, message="Invalid credentials.")

#Creating a refresh token so user will not have to re-login again
@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, expires_delta=timedelta(hours=2))

        return {"access_token": new_token}

#Logout Function
@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}
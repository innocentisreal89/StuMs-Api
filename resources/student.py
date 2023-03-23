from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.student import Student, calculate_gpa
from models.registered_course import RegisteredCourse
from models.admin import admin_required
from db import db
from schemas import *
from schemas import StudentRegSchema,StudentUpdateSchema
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import jwt_required, get_jwt_identity




blp =  Blueprint('Students', 'students', description='Operation on Students')


#   Get student Details with  the student email, so that student can get their login detail
@blp.route('/student_id/<string:email>')
class GetStudent(MethodView):
    @blp.response(200, StudentOutputSchema)
    @blp.doc(description='Get a student\'s stud_id (i.e matric number) by email')
    def get(self,email):
        student = Student.query.filter_by(email=email).first()
        if not student:
            abort(404, message='Student Not Found')
        return student

#get a logged in student to view his detials--  student only
@blp.route('/student_id')
class GetStudent(MethodView):
    @blp.response(200, StudentDataSchema)
    @blp.doc(description='Get an authenticated student\'s profile')
    @jwt_required()
    def get(self):
        matric_no = get_jwt_identity()
        student = Student.query.filter_by(matric_no=matric_no).first()
   
        return student

    #   To change password   ---Student only
    @blp.arguments(UpdateStudentPassword)
    @blp.doc(description='Update a student\'s password')
    @jwt_required()
    def patch(self, password_data):
        matric_no = get_jwt_identity()
        student = Student.query.filter_by(matric_no=matric_no).first()

        #This handle the logic for updating password
        if password_data['new_password']:
            if password_data['confirm_password']:
                if password_data['new_password'] != password_data['confirm_password']:
                    abort(401, message="Password do not Match.")
            else:
                abort(403, message="Please Confirm your Password")
        else:
            abort(403, message="Please Input Password")

        password = pbkdf2_sha256.hash(password_data['new_password'])
        student.password = password 
        student.reset_password = True
        db.session.commit()
        return {'message':'Password Updated Successfully'},200





#   Admin only
"""
    Note: while creating the student due to the random generator, which a better solution will be profer
    to this effect. the admin might have to load/ post the student data even after receiving an integrity error.
    to avoid this the code geneartor should be increased 
"""
#   Register and get all student
@blp.route('/register-student')
class RegisterStudent(MethodView):
    @jwt_required()
    @admin_required
    @blp.arguments(StudentRegSchema)
    @blp.response(201, PlainStudentSchema)
    @blp.doc(description='Register a Student')
    def post(self, student_data):
        student = Student.query.filter_by(email=student_data['email']).first()
        if student:
            abort(400, message="An Student with that email already exists.")
        student = Student(
            firstName = student_data['firstName'].lower(),
            lastName = student_data['lastName'].lower(),
            email = student_data['email'].lower(),
            gender = student_data['gender'].lower(),
            department = student_data['department'].lower(),
            faculty =student_data['faculty'].lower(),
            degree = student_data['degree'].upper(),
            level = student_data['level'].lower(),
            semester = student_data['semester'].lower(),
        )
        student.save()
        return student

    
    #   To get all Student
    @jwt_required()
    @admin_required
    @blp.response(200, PlainStudentSchema(many=True))
    @blp.doc(description='Get all students',
             summary='Get all registered students with their details')
    def get(self):
        students = Student.query.all()
        
        return students

#   ADMIN 
#   Get,Upload and Delete Student per id
@blp.route('/student/<string:matric_no>')
class GetUpdateDeleteStudent(MethodView):
    @jwt_required()
    @admin_required
    @blp.response(200,StudentDataSchema)
    @blp.doc(description='Get a student details by matric_no')
    def get(self,matric_no):
        student = Student.query.filter_by(matric_no=matric_no).first()
        if not student:
            abort(404, message='Invalid Student Id')
        return student
    
    @jwt_required()
    @admin_required
    @blp.arguments(StudentUpdateSchema)
    @blp.response(200, StudentDataSchema)
    @blp.doc(description='Update a student details by matric_no')
    def put(self, student_data, matric_no):
        student = Student.query.filter_by(matric_no=matric_no).first()
        if not student:
            abort(404, message='Student Not Found')
        
        student.department = student_data['department'].lower()
        student.faculty = student_data['faculty'].lower()
        student.degree = student_data['degree'].upper()
        student.level = student_data['level'].lower()
        student.semester = student_data['semester'].lower()
        
        db.session.commit()
        return student
    
    @jwt_required()
    @admin_required
    @blp.doc(description='Delete a student details by matric_no')
    def delete(self, matric_no):
        student = Student.query.filter_by(matric_no=matric_no).first()
        if not student:
            abort(404, message='Student Not Found')

        student.delete()
        return {'message':'Student Deleted Successfully'},200


#For getting all the grades for all  student offered course --student only
@blp.route('/student/courses-grade/')
class StudentRegisteredCourse(MethodView):
    @jwt_required()
    @blp.response(200, ListStudentRegisteredCourse(many=True))
    @blp.doc(description='Get a student course details by matric_no',
             summary='This display all the course datails with grade')
    def get(self):
        matric_no = get_jwt_identity()
        registered_course = RegisteredCourse.query.filter_by(matric_no=matric_no).all()
        if not registered_course:
            abort(404, message=' Student Not Found')
        
        return registered_course


#Calulation of Student GPA
@blp.route('/student/gpa/<string:matric_no>')
class StudentGpaCalculation(MethodView):
    @jwt_required()
    @admin_required
    @blp.doc(description='Get a student GPA',
             summary='This display the GPA of a student using a 4 point grading system')
    def patch(self,matric_no):
        student = Student.query.filter_by(matric_no=matric_no).first()
        if not student:
            abort(404, message=' Student Not Found')
        registered_course_grade = RegisteredCourse.query.filter_by(matric_no=matric_no).all()

        gpa = calculate_gpa(registered_course_grade)
        student.gpa = gpa 
        db.session.commit()
        return {'message':f'Upload Success, GPA is {gpa}'}
    








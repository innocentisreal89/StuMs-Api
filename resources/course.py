from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.course  import Course
from models.student import Student
from models.admin import AdminModel,admin_required
from models.registered_course import RegisteredCourse
from schemas import *
from db import db
from schemas import CourseRegSchema,CourseUpdateSchema,CourseSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

blp =  Blueprint('Courses', 'courses', description='Operation on Courses')

#   Admin Only
#   Register a Course
@blp.route('/course')
class RegisterCourse(MethodView):
    @jwt_required()
    @admin_required
    @blp.arguments(CourseRegSchema)
    @blp.response(201, PlainCourseSchema)
    def post(self, course_data):
        course = Course.query.filter_by(course_code=course_data['course_code']).first()
        if course:
            abort(400, message="A Course with that Code already exists.")
        course = Course(
            course_title = course_data['course_title'].lower(),
            course_code = course_data['course_code'].upper(),
            course_unit = course_data['course_unit'],
            teacher = course_data['teacher'].lower(),
        )

        course.save()
        return course
    
    #Get all registered course      -- Both Admin and Student have access here
    @jwt_required()
    @blp.response(200, CourseDisplaySchema(many=True))
    def get(self):
        courses = Course.query.all()
        if not courses:
            abort(400, message="No course exist.")
        return courses

#   Get, Upload and Delete a Course
@blp.route('/course/<string:course_code>')
class GetUpdateDeleteCourse(MethodView):
    @jwt_required()
    @admin_required
    @blp.response(200, CourseDisplaySchema)
    def get(self, course_code):
        course = Course.query.filter_by(course_code=course_code).first()
        if not course:
            abort(400, message="Course do not exists. Hint: you can try typing it in uppercase")
        return course

    #   Upload a course
    @jwt_required()
    @admin_required
    @blp.arguments(CourseUpdateSchema)
    @blp.response(200, PlainCourseSchema)
    def put(self,course_data, course_code):
        course = Course.query.filter_by(course_code=course_code).first()
        if not course:
            abort(400, message="Course do not exists.")
        
        course.course_title = course_data['course_title'].lower()
        course.course_unit = course_data['course_unit']
        course.teacher = course_data['teacher'].lower()

        db.session.commit()
        return course
    
    #Delete a course
    @jwt_required()
    @admin_required
    def delete(self, course_code):
        course = Course.query.filter_by(course_code=course_code).first()
        if not course:
            abort(404, message='Course Not Found. Hint:course code are in upper case')

        course.delete()
        return {'message':f'<{course_code}> Deleted Successfully'}





#   Upload Student Grades
@blp.route('/course/grade/<string:matric_no>/<string:course_code>')
class GetUploadStudentGrade(MethodView):
    @jwt_required()
    @admin_required
    @blp.arguments(StudentCourseUpdateSchema)
    @blp.response(200, PlainStudentRegisteredCourse)
    def put(self,grade_data, matric_no, course_code):
        student = Student.query.filter_by(matric_no=matric_no).first()
        if not student:
            abort(404, message='Invalid Student Id')
        course = RegisteredCourse.query.filter_by(course_code=course_code.upper()).first() #if this will work o
        if not course:
            abort(404, message='Course Not Registered')

        if grade_data['score'] > 100:
            abort(409, message='Score Limit Exceeded; Score should be within the range 1 to 100')
        course.score = grade_data['score']
        course.course_grade =grade_data['course_grade'].upper()
        course.course_grade_status = grade_data['course_grade_status'].upper()

        db.session.commit()

        return course
    
    
    #Get student Grades for each course
    @jwt_required()
    @admin_required
    @blp.response(200,  StudentRegisteredCourseDisplay)
    def get(self,matric_no, course_code):
        student = Student.query.filter_by(matric_no=matric_no).first()
        if not student:
            abort(404, message='Invalid Student Id')
        course = Course.query.filter_by(course_code=course_code.upper()).first() #if this will work o
        if not course:
            abort(404, message='Course Not Available')

        registered_course = RegisteredCourse.query.filter_by(matric_no=matric_no, course_code=course_code.upper()).first()
        if not registered_course:
            abort(404, message='Course Not Registered')
        return course


#   Get all Admins
@blp.route('/admins')
class RegisterStudent(MethodView):
    @jwt_required()
    @admin_required
    @blp.response(200, AdminSchema(many=True))
    def get(self):
        admins = AdminModel.query.all()
        return admins


#   Get  all student that register a particular -
@blp.route('/courses/students/<string:course_code>')
class StudentRegisteredInCourse(MethodView):
    @jwt_required()
    @admin_required
    @blp.response(200, StudentSchema(many=True))
    def get(self, course_code):
        course = Course.query.filter_by(course_code=course_code).first()
        if not course:
            abort(404, message=' Course Not Found')
        
        return course.students.all()


#   Student Only
#   Student Course Registration
@blp.route('/register-course')
class RegisterCourse(MethodView):
    @jwt_required()
    @blp.arguments(StudentCourseRegSchema)
    @blp.response(200, CourseSchema)
    def post(self,course_data):
        matric_no=get_jwt_identity()
        student = Student.query.filter_by(matric_no=matric_no).first()
        course = Course.query.filter_by(course_code=course_data['course_code'].upper()).first()
        if not course:
            abort(404, message=" Course Not Found.")

        #check if it is registered
        registered_course = RegisteredCourse.query.filter_by(
            course_code=course_data['course_code'].upper(), matric_no=matric_no).first()
        if registered_course:
            abort(403, message=" Course Already Exist.")

        
        register_course = RegisteredCourse(
            student_id = student.id,
            course_id = course.id,
            course_title = course.course_title,
            course_code = course.course_code,
            course_unit = course.course_unit,
            matric_no = student.matric_no,
            # teacher = course.teacher,
        )

        register_course.save()
        return register_course

@blp.route('/course/<string:matric_no>/<string:course_code>/delete')
class DeleteStudentCourse(MethodView):
    #admin required here
    @jwt_required()
    @admin_required
    def delete(self, matric_no,course_code):
        student = Student.query.filter_by(matric_no=matric_no).first()
        if not student:
            abort(404, message='Invalid Student Id')
        registered_course = RegisteredCourse.query.filter_by(matric_no=matric_no, course_code=course_code.upper()).first()
        if not registered_course:
            abort(404, message='Course Not Registered')
        registered_course.delete()
        return {'message':f'<{course_code}> Deleted Successfully from {matric_no}'}
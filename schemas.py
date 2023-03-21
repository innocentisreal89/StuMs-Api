from marshmallow import Schema, fields



class PlainCourseSchema(Schema):
    id = fields.Int(dump_only=True)
    course_title = fields.Str(required=True)
    course_code =fields.Str(required=True)
    course_unit =fields.Int(required=True)
    teacher = fields.Str(required=True)
    score = fields.Float(dump_only=True)
    course_grade =fields.Str(required=True)
    course_grade_status = fields.Str(required=True)
    registered_on = fields.DateTime(dump_only=True)
    

class PlainStudentSchema(Schema):
    id = fields.Int(dump_only=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    matric_no = fields.Str(required=True,dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True,dump_only=True)
    reset_password = fields.Bool(dump_only=True)
    gender = fields.Str(required=True)
    department = fields.Str(required=True)
    faculty = fields.Str(required=True)
    degree = fields.Str(required=True)
    level = fields.Str(required=True)
    semester = fields.Str(required=True,dump_only=True)
    gpa = fields.Float(required=True)
    date_created = fields.DateTime(dump_only=True)
    
class PlainAdminSchema(Schema):
    id = fields.Int(dump_only=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    staff_id = fields.Str(required=True,dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    is_active = fields.Bool(dump_only=True)
    is_admin = fields.Bool(dump_only=True)

class PlainStudentRegisteredCourse(Schema):
    id = fields.Int(dump_only=True)
    course_title = fields.Str(required=True)
    course_code =fields.Str(required=True)
    course_unit =fields.Int(dump_only=True)
    score = fields.Float(required=True)
    course_grade = fields.Str(required=True)
    matric_no = fields.Str(required=True,dump_only=True)
    course_grade_status = fields.Str(required=True)




#   Registrations Schema
class CourseRegSchema(Schema):  #   Handles the Course Registration/Creation---used
    id = fields.Int(dump_only=True)
    course_title =fields.Str(required=True)
    course_code =fields.Str(required=True)
    course_unit =fields.Int(required=True)
    teacher = fields.Str(required=True)

class StudentRegSchema(Schema): #   for Student Reg.---used
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    email = fields.Str(required=True)
    gender = fields.Str(required=True)
    department = fields.Str(required=True)
    faculty = fields.Str(required=True)
    degree = fields.Str(required=True)
    level = fields.Str(required=True)
    semester = fields.Str(required=True)
    

class AdminSignUpSchema(Schema): # For Admin Reg.---used
    id = fields.Str(dump_only=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True ,load_only=True)

class StudentCourseRegSchema(Schema):  # For Stundent Course Reg----used
    course_code =fields.Str(required=True)
    


#   Login Schema
class LoginSchema(Schema): # For Reg.----used
    user_id = fields.Str(required=True)
    password = fields.Str(required=True)




#   Display Schema
class StudentDataSchema(Schema):        #   This is used to display student details to only logged in sudent
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    matric_no = fields.Int(required=True)
    email = fields.Str(required=True)
    reset_password = fields.Bool(dump_only=True)
    gender = fields.Str(required=True)
    department = fields.Str(required=True)
    faculty = fields.Str(required=True)
    degree = fields.Str(required=True)
    level = fields.Str(required=True)
    semester = fields.Str(required=True)
    gpa = fields.Float(required=True)
    date_created = fields.DateTime(dump_only=True)#used

class StudentOutputSchema(Schema):      #   This is used to display few student details at first 
    id = fields.Int(dump_only=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    matric_no = fields.Int(dump_only=True)
    password = fields.Str(required=True)
    department = fields.Str(required=True)
    level = fields.Str(required=True) #used

class AdminSchema(Schema):  #used
    id = fields.Int(dump_only=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    staff_id = fields.Str(required=True,dump_only=True)
    email = fields.Str(required=True)


class CourseDisplaySchema(Schema):   # Id of aa course--used
    id = fields.Int(dump_only=True)
    course_title = fields.Str(required=True)
    course_code = fields.Str(required=True)
    course_unit = fields.Int(required=True)
    teacher = fields.Str(required=True)
    
class StudentDisplaySchema(Schema):  #ID of a student  and will be displayed in every course a student reg.
    id = fields.Int(dump_only=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    matric_no = fields.Int(dump_only=True)
    department = fields.Str(required=True)
    level = fields.Str(required=True) #used

class StudentRegisteredCourseDisplay(Schema):
    course_code =fields.Str(required=True)
    course_unit =fields.Int(dump_only=True)
    score = fields.Float(dump_only=True)
    course_grade = fields.Str(dump_only=True)
    course_grade_status = fields.Str(required=True)
    matric_no = fields.Int(dump_only=True)#used
    
# class StudentSchema(StudentDisplaySchema):
#     # courses = fields.Nested(StudentRegisteredCourseDisplay())
#     courses = fields.List(fields.Nested(StudentRegisteredCourseDisplay()), dump_only=True)  

# #   This Schemas Nest the Id of course and student to display
# class CourseSchema(CourseDisplaySchema):
#     students = fields.List(fields.Nested(StudentRegisteredCourseDisplay()), dump_only=True)
#     # students = fields.List(fields.Nested(StudentDisplaySchema()), dump_only=True)

# # class StudentSchema(StudentDisplaySchema):
# #     courses = fields.List(fields.Nested(CourseDisplaySchema()), dump_only=True)

# class UserSchema(Schema):
#     pass

# #Association schema
# # class StudentCourseRegSchema(Schema):
# #     # course_id = fields.Nested(CourseSchema)
# #     # student_id = fields.Nested(StudentSchema)
# #     id = fields.Int(dump_only=True)
# #     course_title =fields.Str(required=True)
# #     course_code =fields.Str(required=True)
# #     course_unit =fields.Int(required=True)
# #     matric_no = fields.Int(required=True)

class StudentSchema(StudentDisplaySchema):  #used
    courses_registered = fields.Nested(StudentCourseRegSchema(), many=True)

class CourseSchema(CourseDisplaySchema): # used
    students = fields.Nested(StudentCourseRegSchema(), many=True)


class ListStudentRegisteredCourse(Schema): #used
    course_code =fields.Str(required=True)
    course_unit =fields.Int(dump_only=True)
    score = fields.Float(required=True)
    course_grade = fields.Str(dump_only=True)
    course_grade_status = fields.Str(required=True)


#   Update Schemas
class StudentCourseUpdateSchema(Schema):#used
    score = fields.Float()
    course_grade = fields.Str()
    course_grade_status = fields.Str()

    
class CourseUpdateSchema(Schema):  # used
    course_title =fields.Str()
    course_unit =fields.Int()
    teacher = fields.Str()

class StudentUpdateSchema(Schema):# only admin can use this--used
    department = fields.Str()
    faculty = fields.Str()
    degree = fields.Str()
    level = fields.Str()
    semester = fields.Str()
   

# class StudentCourseUpdateSchema(Schema):    #used
#     score = fields.Float()
#     course_grade = fields.Str()
#     course_grade_status = fields.Str()


#update studdent Password
class UpdateStudentPassword(Schema):#used
    new_password =fields.Str(required=True)
    confirm_password =fields.Str(required=True)
    




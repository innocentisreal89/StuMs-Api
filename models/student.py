from db import db
from datetime import datetime
import random
from passlib.hash import pbkdf2_sha256
from flask_smorest import abort


#this handles the matric number generation
def coder_gen(arg:str):
    code = random.randint(1000,9000)
    code = str(arg) + str(code) 
    return code



def default_password(default_password):
    password = pbkdf2_sha256.hash(default_password)
    return password




class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer(), primary_key=True)
    firstName = db.Column(db.String(30), nullable =False)
    lastName = db.Column(db.String(30), nullable =False)
    matric_no = db.Column(db.String(20), unique=True, nullable=False,
                default=coder_gen(20))
    email = db.Column(db.String(30),unique=True, nullable =False)
    password = db.Column(db.Text(), nullable =False,
                default=default_password('password'))
    reset_password = db.Column(db.Boolean(), default=False)
    gender = db.Column(db.String(10), nullable =False)
    department = db.Column(db.String(30), nullable=False)
    faculty = db.Column(db.String(40), nullable =False)
    degree = db.Column(db.String(20), nullable =False, default='BSc')
    level = db.Column(db.String(20), nullable =False, default='100')
    semester = db.Column(db.String(20), nullable =False, default='First')
    gpa = db.Column(db.Float(), nullable=False, default= 0.00)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    # user = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    courses = db.relationship('Course', secondary='registered_courses', back_populates='students', lazy='dynamic')


    def __repr__(self):
        return f'<Student {self.matric_no}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()








def calculate_gpa(arg):
    x=[]
    for grade in arg:
        if grade.course_grade == 'N/A':
            abort(409, message='Incomplete Grade,Please Recheck all Grades for this student ' )
        elif grade.course_grade =='A':
            x.append(4)
        elif grade.course_grade =='B':
            x.append(3)
        elif grade.course_grade =='C':
            x.append(2)
        elif grade.course_grade =='D':
            x.append(1)
        else:
            x.append(0) 
    units=[]
    total_unit=0
    for unit in arg:
        y = unit.course_unit
        units.append(y)
        total_unit += y

    total_weight = [_ * i for _, i in zip(x, units)]
    gpa = sum(total_weight)/total_unit
    gpa = round(gpa,2)
    return gpa



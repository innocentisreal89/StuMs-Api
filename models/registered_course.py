from db import db
from datetime import datetime

class RegisteredCourse(db.Model):
    __tablename__ = 'registered_courses'
    id = db.Column(db.Integer(), primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'), nullable=False)
    student_id= db.Column(db.Integer(), db.ForeignKey('students.id'), nullable=False)
    course_title = db.Column(db.String(20), nullable=False,default='N/A')
    course_code = db.Column(db.String(20), nullable=False)
    course_unit = db.Column(db.Integer(), nullable=False, default=1)
    score = db.Column(db.Float(precision=2))
    course_grade = db.Column(db.String(20), nullable=False, default='N/A')# e.g, A,B,C,D,F
    matric_no = db.Column(db.Integer(), nullable=False)
    course_grade_status = db.Column(db.String(10),nullable=False,default='N/A') #e.g Passed, Failed
    
 


    def __repr__(self):
        return f'<StudentCourse {self.id}>'
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

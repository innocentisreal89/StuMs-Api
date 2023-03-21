from db import db
from datetime import datetime




class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer(), primary_key=True)
    course_title = db.Column(db.String(20), nullable=False ,default='N/A')
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_unit = db.Column(db.Integer(), nullable=False, default=1)
    teacher = db.Column(db.String(30), nullable=False, default='N/A')
    registered_on = db.Column(db.DateTime(), default=datetime.utcnow)
    students = db.relationship('Student', secondary='registered_courses',back_populates='courses', lazy='dynamic' )
   


    def __repr__(self):
        return f'<Course {self.id}>'


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    



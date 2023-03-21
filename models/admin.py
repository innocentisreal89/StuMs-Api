from db import db
from functools import wraps
from flask_smorest import abort
from datetime import datetime
import operator, random
from flask_jwt_extended import  get_jwt_identity



def code_gen(prefix):
    code = random.randint(1000,90000)
    code = str(code)
    return prefix + code

class AdminModel(db.Model):
    __tablename__ = 'Admins'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(30), nullable=False)
    lastName = db.Column(db.String(30), nullable=False)
    staff_id = db.Column(db.String(30), unique=True, nullable=False,
                default=code_gen(f'ADMIN-UI{datetime.now().year}-'))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean(), default=False)
    is_admin = db.Column(db.Boolean(), default=True)
    # student = db.relationship('Student', backref='users', lazy='dynamic')

    def __repr__(self):
        return f'<Admin {self.email}>'
    

    

    # print(check_last_email_char(email))
    def save(self):
        db.session.add(self)
        db.session.commit()

    
#   This logic for creating a decorator using the wrapper function
def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwarg):
        loggedUser = get_jwt_identity()
        if not loggedUser.startswith('ADMIN-UI'):
            abort(401, message="Restricted Access")
        return function(*args, **kwarg)
    return wrapper

def check_last_email_char(str):
    n = 9
    str2 = operator.getitem(str, slice(len(str)-n, len(str)))
    return str2
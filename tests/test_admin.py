import unittest
from main import create_app, config_dict
from db import db
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token
from models.admin import AdminModel
from models.student import Student




class AdminTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context()
        self.appctx.push() #to push our context to the app
        self.client = self.app.test_client()        # for us to be able to test our route

        db.create_all() #this create the data in the memory

        #Test data  --- we will make reference to it RUD oprations only
        student = Student(
            firstName="israel",
            lastName="john",
            matric_no=201456,
            email="israel1@gmail.com",
            password=pbkdf2_sha256.hash("password"),
            gender="Male",
            department="Geography",
            faculty="Science",
            degree="BSc",
            level="400",
            semester="First"
        )
        student.save()
        admin = AdminModel(
            firstName="olamidetest",
            lastName="john",
            email="olaidejohn@ui.edu.ng",
            staff_id="ADMIN-UI2023-45130",
            password=pbkdf2_sha256.hash("123456789")
        )
        admin.save()

    def tearDown(self):
        
        db.drop_all() # to drop all existing table if any exist

        self.appctx.pop()   #delete our content from the app
        self.app = None
        self.client = None




    def test_admin_reg(self):
        data = {
            'firstName':'olamidetest',
            'lastName':'john',
            'email':'olapidejohn@ui.edu.ng',
            'password':'123456789'
        }

        response = self.client.post("/register-admin", json=data)
        user = AdminModel.query.filter_by(email=data['email']).first()
        self.assertEqual(response.status_code,201 )
        self.assertEqual(user.firstName, data["firstName"])
        self.assertEqual(user.email, data["email"])


    def test_admin_login(self):
        # test for user login
        admin = AdminModel.query.filter_by(email="olaidejohn@ui.edu.ng").first()
        user_id = admin.staff_id
        data = {
            "user_id": user_id,
            "password": "123456789"
        }
        response = self.client.post("/login", json=data)
        self.assertEqual(response.status_code, 200)

    

    
    def test_register_student(self):
        #dummy data
        data = {
            "firstName": "israel",
            "lastName": "john",
            "email": "israel2@gmail.com",
            "gender": "Male",
            "department": "Geography",
            "faculty": "Science",
            "degree": "BSc",
            "level": "Level_400",
            "semester": "First"
        }

        token = create_access_token(identity="ADMIN-UI2023-45130")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.post("/register-student", json=data, headers=headers)
        self.assertEqual(response.status_code, 201)

        students = Student.query.all()

        student_id = students[0].id
        assert student_id == 1
        self.assertNotEqual(response.json['email'], students[0].email)
        students = Student.query.filter_by(id=1).first()
        assert students.department == 'Geography'

    

    def test_get_all_students(self): 
        token = create_access_token(identity='ADMIN-UI2023-45130')
        header = {
            "Authorization":f"Bearer {token}"
        }
        response = self.client.get('/register-student', headers=header)
        self.assertEqual(response.status_code, 200)
     


    def test_get_each_student(self):
        student = Student.query.filter_by(email="israel1@gmail.com").first()
        matric_no = student.matric_no

        token = create_access_token(identity="ADMIN-UI2023-45130")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get(f"/student/{matric_no}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['firstName'], 'israel')


    def test_update_student_data(self):

        student = Student.query.filter_by(matric_no=201456).first()
        matric_no= student.matric_no

        token = create_access_token(identity="ADMIN-UI2023-45130")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        data = {
            "level": "200",
            "department": "physics",
            "semester": "second",
            "faculty": "science",
            "degree": "BSC"
        }
        response = self.client.put(f"/student/{matric_no}",headers=headers,json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(student.level, '200')
        self.assertEqual(student.department, 'physics')


    def test_get_all_admins(self): 
        token = create_access_token(identity='ADMIN-UI2023-45130')
        header = {
            "Authorization":f"Bearer {token}"
        }
        response = self.client.get('/admins', headers=header)
        self.assertEqual(response.status_code, 200)



    





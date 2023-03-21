import unittest
from main import create_app
from config.config import config_dict
from db import db
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256
from models.student import Student



class StudentTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context()
        self.appctx.push() #to push our context to the app
        self.client = self.app.test_client()        # for us to be able to test our route

        db.create_all() #this create the data in the memory

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
            level="Level_400",
            semester="First"
        )
        student.save()


    def tearDown(self):
        
        db.drop_all() # to drop all existing table if any exist

        self.appctx.pop()   #delete our content from the app
        self.app = None
        self.client = None


    """
        here is how it works:
        if u run dis test first, it creates that table in the memory, if you want to run it again, it has existing table and you dont
        want to start creating the table again, so once you run it, it drops all the table u have previously and run it again 
    """


    # def test_student_login(self):
    #     data = {
    #         'user_id':'206555',
    #         'password':'password'
    #     }
    #     response = self.client.post('/login', json=data)
    #     assert response.status_code == 200

    def test_admin_login(self):
        # test for user login
        student = Student.query.filter_by(email="israel1@gmail.com").first()
        user_id = student.matric_no
        data = {
            "user_id": user_id,
            "password": "password"
        }
        response = self.client.post("/login", json=data)
        self.assertEqual(response.status_code, 200)

    def test_get_student_profile(self):
        """Test that an authenticated student can retrieve their profile"""
        # Create an access token for the test student
        student = Student.query.filter_by(email="israel1@gmail.com").first()
        current_user = student.matric_no
        token = create_access_token(identity=current_user)
        header = {
            "Authorization": f"Bearer {token}"
        }
        
        # Send a GET request to the /student-profile endpoint with the access token
        response = self.client.get("/student_id",headers=header)

        self.assertEqual(response.status_code, 200)

    def test_patch_student_password(self):
        """Test that an authenticated student can update their password"""
        # Create an access token for the test student
        student = Student.query.filter_by(email="israel1@gmail.com").first()
        current_user = student.matric_no
        token = create_access_token(identity=current_user)
        header = {
            "Authorization": f"Bearer {token}"
        }
        
        password_data = {"new_password": "newpassword","confirm_password": "newpassword"}
        # Send a PATCH request to the student endpoint with the access token and new password data
        response = self.client.patch("/student_id",headers=header,json=password_data)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)
        self.assertTrue(pbkdf2_sha256.verify("newpassword", student.password))


    def test_register_course(self):
        """Test that an authenticated student can register a course"""
        # Create an access token for the test student
        student = Student.query.filter_by(email="israel1@gmail.com").first()
        current_user = student.matric_no

        data = {
            "course_code": "BIO101"
        }

        token = create_access_token(identity=current_user)
        header = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.post("/register-course", json=data, headers=header)
        self.assertEqual(response.status_code, 404) # course did not exist

    def test_get_student_id(self):
        """Test that a registered student can get their student id """

        response = self.client.get("/student_id/israel1@gmail.com")

        student = Student.query.filter_by(email="israel1@gmail.com").first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(student.matric_no, "201456")
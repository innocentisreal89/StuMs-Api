import unittest
from main import create_app,config_dict
from db import db
from models.course import Course
from flask_jwt_extended import create_access_token



class CourseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()

        #Test data  --- we will make reference to it RUD oprations only
        course = Course(
                course_code="PHY301",
                course_title="Classical Physics",
                course_unit=3,
                teacher="Dr. Ogunseye"
        )
        db.session.add(course)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None

    #   PASSED
    def test_create_course(self):
        data = {
            "course_code": "MAT309",
            "course_title": "Advanced Differential Equation",
            "course_unit": 3,
            "teacher": "Prof. Janet",
        }

        # create JWT token for authorization
        token = create_access_token(identity="ADMIN-UI2023-45130")

        # set headers with JWT token
        header = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.post("/course", json=data, headers=header)

        self.assertEqual(response.status_code, 201)
    

        """
            we made use of assertEqual() because it tests if two values are equal:
            If the first value does not equal the second value, the test will fail.
        """


        # Check if course was created and also check the initial test data
        courses = Course.query.all()
        self.assertEqual(courses[0].id, 1)
        self.assertEqual(courses[0].course_unit, 3)
        self.assertEqual(courses[1].course_code, "MAT309")



    def test_get_all_courses(self):
        token = create_access_token(identity='ADMIN-UI2023-45130')
        header = {
            'Authorization':f'Bearer {token}'
        }
        response = self.client.get("/course", headers=header)
        self.assertEqual(response.status_code, 200)
        

    
    def test_get_specific_course(self):
        # # create JWT token for authorization
        token = create_access_token(identity="ADMIN-UI2023-45130")

        
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.get("/course/PHY301",headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_course_by_id(self):
      
        token = create_access_token(identity="ADMIN-UI2023-45130")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get("/course/PHY301",headers=headers)
        self.assertEqual(response.status_code, 200)


    def test_update_course(self):
        data = {
            "course_title": 'Intro to Astronomy',
            "course_unit": 3,
            "teacher": "Dr. Franklin"
        }

        # create JWT token for authorization
        token = create_access_token(identity="ADMIN-UI2023-45130")

        # set headers with JWT token
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.put("/course/PHY301", json=data, headers=headers)
        self.assertEqual(response.status_code, 200)

        course = Course.query.filter_by(course_code="PHY301").first()
        self.assertEqual(course.course_unit, 3)
        self.assertEqual(course.teacher, "dr. franklin")
        self.assertEqual(course.course_title, "intro to astronomy")
        self.assertNotEqual(course.course_unit, 2)
        self.assertNotEqual(course.teacher, "dr. ogunseye")

    def test_delete_course(self):
        # create JWT token for authorization
        token = create_access_token(identity="ADMIN-UI2023-45130")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = self.client.delete("/course/PHY301", headers=headers)
        self.assertEqual(response.status_code, 200)
        course = Course.query.all()
        self.assertEqual(len(course), 0)
        self.assertEqual(course, [])
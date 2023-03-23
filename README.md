# StuMs-Api

<a name="readme-top"></a>

-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<!-- <br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Best-README-Template</h3>

  <p align="center">
    An awesome README template to jumpstart your projects!
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
</div> -->



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About StuMs-API</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About StuMs-API

<strong>StuMs-API</strong> is a Student Management System API, hence the coinage of the world
StuMs. It is a restful API built with Flask-Smorest. This Api has two users; the student and admin. Their usage will be given below: 
where the student has the priviledge to register for an available course and check their details while the admin handles the

## Admin
* Admins can create, read, update and delete students, student registered courses and courses  
* Admins can view all students and courses
* Admins can view all students registered for a course
* Admins can view all courses a student registered for
* Admins can update student's details such as the level, semester, department, etc.
* Admins can upload student's grade for each course
* Admins can upload student's GPA

## Student
* Students will first get their unique student ID by using their email to fetch it
* Students can login with their student ID and a default password and view their profiles
* Students can register for courses and  get to view registered courses
* Student can reset their password


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [![Python][Python]][https://www.python.org/downloads/]
* [![Flask][Flask]][Flask-url]
* [![Flask-Smorest][Flask-Smorest]][Flask-Smorest-url]
* [![SQlite][SQlite]][SQlite-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>




## Getting Started


### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Python3: 
    ```sh
    [Get Python](https://www.python.org/downloads/)
    ```

### Installation


1. Clone this repo
   ```sh
   git clone https://github.com/innocentisreal89/StuMs-Api.git
   ```
2. Navigate into the directory
   ```sh
   cd StuMs-Api
   ```
3. Create a virtual environment
   ```sh
   py -3 -m venv venv_name
   ```
4. Activate the virtual environment on powershell or git bash for windoows
   ```sh
   venv_name\Scripts\activate.bat
   ```
   On Bash ('bin' for linux)
   ```sh
   source venv_name/Scripts/activate.csh
   ```
5. Install project dependencies
   ```sh
   pip install -r requirements.txt
   ```
6. Set environment variables
   ```sh
   $env:FLASK_APP='main.py'
   ```
   On Bash
   ```sh
   export FLASK_APP=run.py
   ```
   
7. Set the create_app function to run the app in development mode.
   Make sure the imported create_app function in the main.py looks like this
   ```sh
   app = create_app()
   ```
   and not like this
   ```sh
   app = create_app(config=config_dict['prod'])
   ```

8. Create database
   ```sh
   flask shell
   ```
   ```sh
   >>> db.create_all()
   >>> exit()
    ```
 
8. Run Flask
   ```sh
   flask run
   ```
   or
   ```sh
   python runserver.py
   ```
9. Use the link generated on the terminal to access the endpoints
    ```sh
   http://127.0.0.1:5000
   ```
   To use swagger-ui, use the link below
   ```sh
    http://127.0.0.1:5000/swager-ui
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- CONTACT -->
## Contact

Israel Innocent - [@G_Science1](https://twitter.com/G_Science1) - innocentisreal8@gmail.com <br>

Project Link: [StuMs-API](https://github.com/innocentisreal89/StuMs-Api)<b>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Alt School Alfrica](https://altschoolafrica.com/schools/engineering)
* [Stack Overflow](https://stackoverflow.com/)
* [Othneil Drew's README Template](https://github.com/othneildrew/Best-README-Template)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

[linkedin-url]: https://img.shields.io/badge/in/israel-innocent-a76946230-1ca0f1?style=for-the-badge&logo=linkedin&logoColor=blue&link=https://www.linkdin.com/in/israel-innocent-a76946230

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/innocentisreal89/StuMs-Api.svg?style=for-the-badge
[contributors-url]: https://github.com/innocentisreal89/StuMs-Api/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/innocentisreal89/StuMs-Api.svg?style=for-the-badge
[forks-url]: https://github.com/innocentisreal89/StuMs-Api/network/members
[stars-shield]: https://img.shields.io/github/stars/innocentisreal89/StuMs-Api.svg?style=for-the-badge
[stars-url]: https://github.com/innocentisreal89/StuMs-Api/stargazers
[issues-shield]: https://img.shields.io/github/issues/innocentisreal89/StuMs-Api.svg?style=for-the-badge
[issues-url]: https://github.com/innocentisreal89/StuMs-Api/issues
[license-shield]: https://img.shields.io/github/license/innocentisreal89/StuMs-Api.svg?style=for-the-badge
[license-url]: https://github.com/innocentisreal89/StuMs-Api/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/israel-innocent
[twitter-shield]: https://img.shields.io/badge/-@G_Science1-1ca0f1?style=for-the-badge&logo=twitter&logoColor=white&link=https://twitter.com/G_Science1
[twitter-url]: https://twitter.com/G_Science1
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[flask]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white

Welcome to the FaceRecognition Attendance System, a cutting-edge solution for efficient and secure attendance tracking. This system leverages advanced facial recognition technology to streamline the attendance process, making it both accurate and user-friendly. This face Recognition based Attendance system is a Django application written in Python, HTML and CSS.
 Features:
 Administration and Students have different roles to do in our website.
 Roles of Administration
      1. Administration can add new students.
      2. After logging in, Administration can upload image file/files of class to generate attendance.
      3. After uploading the files, attendance marking will be processed in the backend and  after it is processed, they will be redirected to the courses page where they can download   attendance file and can view average attendance in each course.
      4. There is an Edit Attendance page where administration can change the attendance status of some students by entering their roll numbers at a particular date to present/absent if there are some inaccuracy conditions.
      
  Roles of Students
1. Students can login to the website through their roll numbers as usernames and passwords.
       2. Students can only see their attendance percentage in a particular course.

 Files & Directories:
 - `Face_recognition` - Project directory.
         -`Attendance`
                 -`templates` 
                        -`attendance.csv`   -  Attendance file
                        -`courses.html`   -  Courses page(can download attendance file)
                        -`courses2.html`   -  Student's attendance percentage
                        -`edit.html`   -   Edit attendance page(accessible only to the adminstration)
                         -`home.html`    -   Home page
                         -`login.html`     -   Login page
                         -`profile.html`   -  User Profille page
                         -`signup.html`   -  Sign Up page
                   -`admin.py`    -  Contains some models for access to the Django administrator.
                   -`apps.py`    -   Contains some apps from Django
                   -`forms.py`   -   forms from Django
                   -`models.py`   -  All models used in the application are created here.
                   -`tem.py`    -    To create a new csv file 
                   -`urls.py`     -   This file handles all the URLs of the web application.
                   -`views.py`   -   This file contains all the application views.
          -`Face_recognition`
	     -`asgi.py`   -    ASGI config for Face Recognition Project
	     -`settings.py`   -  Settings for Face Recognition Project
	     -`urls.py`   -   This file handles all the URLs of the project.
	     -`wsgi.py`   -   WSGI config for Face Recognition Project
          -`imgs`   -   dataset images of all students
          -`media`   -   dataset images of all students stored in database
          -`db.sqlite3`   -   Database used to store all the data
          -`manage.py`   -    This file is used basically as a command-line utility and for deploying, debugging, or running our web application.
          -`requirements.txt`  -   This file contains all contains all the python packages that needs to be installed to run this web application.

 Installation:
•	Install Python3.9 from [here](https://www.python.org/downloads/) manually.
•	Install project dependencies by running `py -m pip install -r requirements.txt`.
•	Open a new terminal and run the command `cd Face_recognition` to open the folder
•	Run the commands `py manage.py makemigrations` and `py manage.py migrate`  in the project directory to make and apply migrations.
•	Create superuser with `py manage.py createsuperuser`. This step is optional.
•	Run the command `py manage.py runserver` to run the web server.
•	It takes a while to process the encodings of the dataset faces and generate url.
•	Open web browser and goto `127.0.0.1:8000` url to start using the web application.
•	For logging in as teacher, you must have a superuser account. You can create super user using command `py manage.py createsuperuser` in the terminal after opening Face_recognition folder(`cd Face_recognition`). We have already created a superuser. You can use that:
   Username: face
   Password: face
•	For logging in as student, you must enter username and password as your roll number.


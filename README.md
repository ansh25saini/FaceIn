# <img src="https://user-images.githubusercontent.com/103529456/170893819-f4b6df3f-e694-4681-a0a3-673835c46db4.png" alt="logo" style="width:150px; height: 75 px;"/>

### FaceIn is a web application which utilizes facial recognition to mark the attendance, time-in, and time-out of users. It has been built as the solution to Microsoft Engage Challenge 2022.

<img src="https://user-images.githubusercontent.com/103529456/170894197-9d87d187-5cfa-40d3-914e-8c512d4ffae2.png" alt="home" width="1432"/>

## 🔗 Relevant Links

* [Project Presentation](https://docs.google.com/presentation/d/1XrVbKZQre8eamJLUHPqG04YYsS9nyUTa/edit?usp=sharing&ouid=113134786751553039333&rtpof=true&sd=true)
* [Project Report](https://docs.google.com/document/d/1gH98lipxY5vzZ3dLxMudkOj4zZ4w7qgX/edit?usp=sharing&ouid=113134786751553039333&rtpof=true&sd=true)
* [Video Demo](https://drive.google.com/file/d/129QO52wrJGVjx_cgrzuV_Y1SsOCduPY9/view?usp=sharing)


## 📌 Table of Contents
* [Features](#features)
* [Tech Stack / Dependencies](#tech-stack)
* [Architecture](#architecture)
* [Agile Development Methodolgy](#agile)
* [Getting Started/ Setup](#getting-started)
* [Passwords](#passwords)
* [User Guide](#📖-user-guide)
* [Challenges Faced and Learnings](#💡-challenges-faced-and-learnings)
* [Limitations and Scope](#scope)
* [Bug Reporting](#bug)
* [Feature Request](#feature-request)


<a id="features"></a>
## 🚀 Features
- Actionable and simple UI. 
- Signing In using basic username/password method, provided by organization to the user.
- Ability to mark real time attendance.
- Send instant email whenever the attendance is marked in/out.
- Show attendance analytics to the user.
- Show attendance anaytics of the organization to the admin.
- Accuracy of the model is more than 99%.
- Django default admin panel also customized, in accordance with the website design.
- Automatic disappearing of notification messages like "You are now logged in", exactly after 4 seconds.
- Update user profile option, provided in the admin-dashboard.
- Contact form provided to raise any type of query that anyone may have.
- Instant email notification to admin whenever someone fills the contact form.
- Use of PostgreSQL Database.
- Completely Responsive Website.
- [Add more features](#feature-request)...


<a id="tech-stack"></a>
## 💻 Tech Stack / Dependencies

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)

***Python*** : The complete project is written in python programming language.

***OpenCV*** : OpenCV and imutils have been used for image processing.

***Django*** : Open-source python based web framework that uses MVT architectural pattern, is used.

***PostgreSQL*** : Open-source relational database management system used in this project

***VIsual Studio Code*** : Editor used in the project

<a id="architecture"></a>
## 🪢 Architecture

<img width="705" alt="architecture" src="https://user-images.githubusercontent.com/103529456/170905732-b4faa2b4-122a-4940-9ee7-d36df18f380a.png">

<img width="705" alt="architecture2" src="https://user-images.githubusercontent.com/103529456/170906025-38bc43b1-219d-4617-9282-c76b3ec2a971.png">


<a id="agile"></a>
## ⚡️ Agile Development Methodology

I followed Agile Development Methodology to complete the project. Agile is an easy to handle and flexible development process which relies on light(short-termed) planning procedures. It allows faster adjustments and reviewing with an aim of keeping the principle of zero bug bounce.
The complete task has been completed in 4 sprints, as depicted in the images below:

<img width="705" alt="agile-1" src="https://user-images.githubusercontent.com/103529456/170895598-4d784122-8224-4639-afd3-0265091d049b.png">

<img width="707" alt="agile-2" src="https://user-images.githubusercontent.com/103529456/170895600-ec5b5091-f144-49a1-9bea-ad1a6dd172c9.png">


<a id="getting-started"></a>
## 📦 Getting Started/ Setup

1. Clone this repository.

```javascript
  git clone https://github.com/ansh25saini/FaceIn.git
```  

2. Make and activate the virtual environment *env*

```javascript
  python -m venv env
  env/Scripts/activate
```

3. Before installing requirements.txt, install cmake because without dlib cannot be installed and there will be a error, so, 

```javascript
   pip install cmake==3.22.4
```

4. After that install dlib==19.24.0
  
  ```javascript
   pip install dlib==19.24.0
  ```
  
5. After installing dlib and cmake, install rest,

  ```javascript
   pip install -r requirements.txt
  ```

6. Do the following command one by one

  ```javascript
   python manage.py makemigrations
   python manage.py migrate
  ```
      
7. go to *env/Lib/site-packages/imutils/face_utils/facealigner.py* file and change the syntax of eyesCenter (in my file it is in 64th line)
  * from this
  ```javascript
   eyesCenter = ((leftEyeCenter[0] + rightEyeCenter[0]) // 2,
            (leftEyeCenter[1] + rightEyeCenter[1]) // 2)
  ```
  * to this
  ```javascript
  eyesCenter = (int((leftEyeCenter[0] + rightEyeCenter[0]) // 2),
            int((leftEyeCenter[1] + rightEyeCenter[1]) // 2)
  ```
  Make sure you follow *correct indentation* (of 2 spaces, as original one) 
  while  changing the above syntax; and finally save the file;

  Without the int keyword, *can't parse 'center'. Sequence item with index 0 has a wrong type*, error will be shown while taking images.

8. Finally to run the project,
  ```javascript
  python manage.py runserver
  ```
<a id="passwords"></a>
## 🔑 Passwords

* Admin
   * username- admin@facein
   * password- facein123
   * email-id- ansh25saini@gmail.com

* User-1
   * username- e01
   * password- e01
   
* User-2
   * username- e02
   * password- e02

* Website Gmail Account
   * email- noreplyfacein@gmail.com
   * password- facein123

* PostgreSQL account-
  ```javascript
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'facein_db',
        'USER': 'postgres',
        'PASSWORD': 'ansh123',
        'HOST': 'localhost',
    }
  }
  ``` 

<a id="user Guide"></a>
## 📖 User Guide

### Home Page 
This is the home page, the nav bar area contains About, Services, Contact, Login section.

All links on every page are completely working.

<img width="1432" alt="Home-2" src="https://user-images.githubusercontent.com/103529456/170899014-fe75296c-a01a-4066-bf81-0ddbf37aab94.png">

### About Page
Tells about what FaceIn is, its customers and their valuable reviews. 

<img width="1436" alt="about-1" src="https://user-images.githubusercontent.com/103529456/170898991-7c2a6c8d-bb21-42ce-8be3-6054a98e7297.png">
<img width="1436" alt="about-1" src="https://user-images.githubusercontent.com/103529456/170898992-c952c8be-a451-4d70-8289-792a5d76c06c.png">

### Services Page
Shows our services as well as contain a demo video on how to use FaceIn.

<img width="1440" alt="services" src="https://user-images.githubusercontent.com/103529456/170899022-72464a35-c7e8-48e3-bead-5ae78b7dec50.png">

### Contact Page
To raise any type of query. An instant mail is sent to admin when-ever someone fills this form.

<img width="1440" alt="contact1" src="https://user-images.githubusercontent.com/103529456/170899006-3cfaee9c-6ad6-4ac3-a730-de551749abc6.png">
<img width="1440" alt="contact2" src="https://user-images.githubusercontent.com/103529456/170899007-bafd00a8-b3ae-47fa-b362-98fe5aa313be.png">

This message gets popped up whenever someone fills the form, similar message also pops up when someone log-in , mark the attendance etc. It automatically disppears after 4 seconds.

<img width="1440" alt="message" src="https://user-images.githubusercontent.com/103529456/170899018-1a3b8896-fa45-40d9-b62b-02cd642f9d89.png">

This is the mail, admin gets from faceIn Website when somebody inquires about something. Similar mail in case of marking-in/out.

<img width="1440" alt="mail" src="https://user-images.githubusercontent.com/103529456/170901829-24abded0-2cb6-4131-ba70-bb9552eb316a.png">

### Login Page
Common for both user and admin. Only admin can register any user and the user has to enter that same id, password to login.

<img width="1440" alt="log-in" src="https://user-images.githubusercontent.com/103529456/170899017-46eef49c-d840-4245-8fec-72e24fb3e68c.png">

### User Dashboard Page
Three functionalities are present- Mark-in/Mark-out/Analytics
* Mark-in/Mark-out- 
     * To check the email functionality, enter your correct email address to get the email notification from noreplyfacein@gmail.com
     * To mark the attendance, only one correct user can be identified at a time with correct login credentials; if frame conatins more than one user 
     at a time whose faces can be recognized then an unauthorized message will be shown.
     So to mark, enter correct username of yours and only you should be in the frame.
    * Press p after you think that you have been correctly recognized by the system
    * Video feed will not close until you press p.
     
<img width="1440" alt="user_dashboard" src="https://user-images.githubusercontent.com/103529456/170899023-5c861030-b65b-4d41-9343-f95331576033.png"> 

<img width="1440" alt="mark-in" src="https://user-images.githubusercontent.com/103529456/170902867-4ebe5ef3-bf97-4389-abfc-9218624bf082.png"> 

### Admin Dashboard Page
1. New Registration: Provided with register, add images and train dataset, button. 
 * For Training option:
    * Training happens of all the users in one go. 
    * Be patient and don't refresh in between. 
    * After complete training, a new window will automatically pop up showing the results.  
 * For Add Image option:
    * Images have to be captured in real environment so as to tackle the effect of brightness on recognition.
    * 30 images are captured in one go and stored in the database.

<img width="1440" alt="admin_dashboard_features" src="https://user-images.githubusercontent.com/103529456/170899000-a0d7af03-dae5-42b6-ad32-c7d15e2f3b5d.png">   

<img width="1440" alt="register" src="https://user-images.githubusercontent.com/103529456/170899021-bb0b168e-ae02-428e-a4db-8def162c3897.png">

2. Other features: The admin can also see the attendance analytics of the whole organization, update user profile and is also provided with a demo video to clear all doubts.

<img width="1440" alt="admin_dashboard_others" src="https://user-images.githubusercontent.com/103529456/170899001-5dc4b785-56b7-4b7e-bd68-ce0d059520bb.png">  

<img width="1440" alt="admin_dashboard_others" src="https://user-images.githubusercontent.com/103529456/170898995-7a9c978e-1f49-4be6-a3f6-3333888825cb.png"> 

### Admin Django Panel
The default django-administartion has been customized according to the website style. Morever, features, reviews, current customers are dynamic and can be changed through this panel.

To go to admin panel, use */admin* in the web address.

<img width="1440" alt="admin_panel-2" src="https://user-images.githubusercontent.com/103529456/170901135-0912facc-451c-4553-9b71-99055812530b.png"> 

As you can see all details are properly present in an organized way, same is the case with other information as well
<img width="1440" alt="adminpanel2" src="https://user-images.githubusercontent.com/103529456/170901066-2cdae3e1-dc1d-49c2-a48b-0ade04f6915e.png"> 

### Responsive Website
The website is completely responsive.
<img width="1440" alt="responsive webpage" src="https://user-images.githubusercontent.com/103529456/170903833-f0fa2a04-7f14-4a5e-b16d-b95146db4fbc.png"> 

<a id="challenges"></a>
## 💡 Challenges faced and learnings

- Spent several hours learning the MVT architecture of Django and Face Recognition Models and then began the design-build process of this project.
- Never implemented any ML model in a web application, so learnt about the same and implemenetd it.
- Came across a major fault in design:- presence of the register button on the home page. I realized that in this way any user, outside the organizaton can register, so changed the design. 
- Found a major error that app was recognizing and marking attendance of anybody (if the user was already registered) that was in the frame, even if the credentials were of different user. Changed the python code, so that only user whose has logged in can be marked.
- Learnt about PostgreSQL Database

<a id="scope"></a>
## 🚧 Limitations and Scope

* Limitations
   * Face recognition accuracy severly gets affected by brightness.- To counter this, many images of the individual are added in one go in real environment conditions and not just a single image, but certainly then also brightness has a role to play.
   * Training a dataset of a large number of users takes a very long time. Though training isn't something that needs to be done frequently, it would be better if a classifier taking less time while maintaining the accuracy can be built.
   * In this project 30 images of each employee are taken for better accuracy. 30 Images per employee in a larger organization can consume a massive volume to store the images.
* Scope
   * The training time can be reduced by retraining the classifier only for the newly added images.
   * A feature can be added where an employee is automatically sent a warning if his attendance or working hours are below the threshold.
   * Downloading attendance as csv file can be implemented.

<a id="bug"></a>
## 🐛 Bug Reporting
Feel free to [open an issue](https://github.com/ansh25saini/FaceIn/issues) on GitHub if you find bugs.

<a id="feature-request"></a>
## ⭐ Feature Request
- Feel free to [open an issue](https://github.com/ansh25saini/FaceIn/issues) on GitHub to add any additional features you feel could enhance this project.  
- You can also discuss and provide suggestions to me on [LinkedIn](https://www.linkedin.com/in/ansh25saini/).

---------
  ```javascript
  if (youEnjoyed) {
      ⭐ starThisRepository();
  }
  ```
-----------
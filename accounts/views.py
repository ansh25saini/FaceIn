from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from matplotlib.animation import FFMpegFileWriter
from face_in.settings import BASE_DIR
from django.db.models import Count
from .models import Present, Time
from .forms import usernameForm,DateForm,UsernameAndDateForm, DateForm_2
from django.core.mail import send_mail

import os
import cv2
import dlib
import math
import numpy as np
import datetime
import time
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rcParams
import imutils
from imutils import face_utils
from imutils.video import VideoStream
from imutils.face_utils import rect_to_bb
from imutils.face_utils import FaceAligner
import pandas as pd
from django_pandas.io import read_frame
from pandas.plotting import register_matplotlib_converters
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.manifold import TSNE

mpl.use('Agg')

##FACE_RECOGNITION_FUNCTIONS

# For add_images function
def dataset_creation(username):
    id = username
    if(os.path.exists('face_files/face_dataset/{}/'.format(id))==False):
        os.makedirs('face_files/face_dataset/{}/'.format(id))
    directory='face_files/face_dataset/{}/'.format(id)

    #Load face detector and the shape predictor for allignment
    print("[INFO] Loading the facial detector")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('face_files/shape_predictor_68_face_landmarks.dat')   
    fa = FaceAligner(predictor , desiredFaceWidth = 96)


    print("[INFO] Initializing Video stream")
    vs = VideoStream(src=0).start()   # Initialize the video stream

    sampleNum = 0
    while(True):
        # Capturing the image
        frame = vs.read() #vs.read each frame

        frame = imutils.resize(frame ,width = 800) #Resize each image

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert to greyscale image
       
        #This will detect all the images in the current frame, and it will return the coordinates of the faces
        faces = detector(gray_frame,0) 

        for face in faces:
            print("For Loop Working")
            (x,y,w,h) = face_utils.rect_to_bb(face)
            face_aligned = fa.align(frame,gray_frame,face)
            # Before capturing the face, we need to tell the script whose face it is,For that we will need an identifier, here we call it id 

            sampleNum = sampleNum+1
            # Saving  only the face part as image dataset            
            if face is None:
                print("None Face")
                continue
            cv2.imwrite(directory+'/'+str(sampleNum)+'.jpg'	, face_aligned)
            face_aligned = imutils.resize(face_aligned ,width = 400)

            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)

            # waitKey of 100 millisecond
            cv2.waitKey(50)

        #Showing the image in another window
        cv2.imshow("Add Images",frame)

        # Give a wait command, otherwise the open cv wont work
        # with the millisecond of delay 1
        cv2.waitKey(1)

        #To get out of the loop
        if(sampleNum>10):
            break

    #Stoping the videostream
    vs.stop()

    # Destroying all the windows
    cv2.destroyAllWindows()

# For train function
def Data_vizualization(embedded, targets,):  
    X_embedded = TSNE(n_components=2).fit_transform(embedded)

    for i, t in enumerate(set(targets)):
        idx = targets == t
        plt.scatter(X_embedded[idx, 0], X_embedded[idx, 1], label=t)

    plt.legend(bbox_to_anchor=(1, 1));
    rcParams.update({'figure.autolayout': True})
    plt.tight_layout()	
    plt.savefig('./face_in/static/img/training_visualisation.png') #Plotting Trained Data Graph
    plt.close()

# For mark_in and mark_out function
def prediction(face_aligned,svc,threshold=0.7):
    face_encodings=np.zeros((1,128))
    try:
        x_face_locations=face_recognition.face_locations(face_aligned)
        faces_encodings=face_recognition.face_encodings(face_aligned,known_face_locations=x_face_locations)
        if(len(faces_encodings)==0):
            return ([-1],[0])

    except:
        return ([-1],[0])

    prob=svc.predict_proba(faces_encodings)
    result=np.where(prob[0]==np.amax(prob[0]))
    if(prob[0][result[0]]<=threshold):
        return ([-1],prob[0][result[0]])

    return (result[0],prob[0][result[0]])

# To update the attendnace for mark_in
def mark_in_update(present):
    today=datetime.date.today()
    time=datetime.datetime.now()
    for person in present:
        user=User.objects.get(username=person)
        try:
           qs=Present.objects.get(user=user,date=today)
        except :
            qs= None

        if qs is None:
            if present[person]==True:
                        a=Present(user=user,date=today,present=True)
                        a.save()
            else:
                a=Present(user=user,date=today,present=False)
                a.save()
        else:
            if present[person]==True:
                qs.present=True
                qs.save(update_fields=['present'])
        if present[person]==True:
            a=Time(user=user,date=today,time=time, out=False)
            a.save()

# To update the attendnace for mark_out
def mark_out_update(present):
    today=datetime.date.today()
    time=datetime.datetime.now()
    for person in present:
        user=User.objects.get(username=person)
        if present[person]==True:
            a=Time(user=user,date=today,time=time, out=True)
            a.save()


def validity_times_check(times_all):
    if(len(times_all)>0):
        sign=times_all.first().out
    else:
        sign=True
        
    times_in=times_all.filter(out=False)
    times_out=times_all.filter(out=True)
    if(len(times_in)!=len(times_out)):
        sign=True
    break_hourss=0
    if(sign==True):
        check=False
        break_hourss=0
        return (check,break_hourss)
    prev=True
    prev_time=times_all.first().time

    for obj in times_all:
        curr=obj.out
        if(curr==prev):
            check=False
            break_hourss=0
            return (check,break_hourss)
        if(curr==False):
            curr_time=obj.time
            to=curr_time
            ti=prev_time
            break_time=((to-ti).total_seconds())/3600
            break_hourss+=break_time
        else:
            prev_time=obj.time

        prev=curr

    return (True,break_hourss)

 # To convert hours to exact hours and minutes                  
def convert_hours_to_hours_mins(hours):
    h=int(hours)
    hours-=h
    m=hours*60
    m=math.ceil(m)
    return str(str(h)+ " hrs " + str(m) + "  mins")

#For analytics of a particular user
def hours_vs_date_username(present_qs,time_qs,admin=True):
    register_matplotlib_converters()
    df_hours=[]
    df_break_hours=[]
    qs=present_qs

    for obj in qs:
        date=obj.date
        times_in=time_qs.filter(date=date).filter(out=False).order_by('time')
        times_out=time_qs.filter(date=date).filter(out=True).order_by('time')
        times_all=time_qs.filter(date=date).order_by('time')
        obj.time_in=None
        obj.time_out=None
        obj.hours=0
        obj.break_hours=0
        if (len(times_in)>0):			
            obj.time_in=times_in.first().time
                
        if (len(times_out)>0):
            obj.time_out=times_out.last().time

        if(obj.time_in is not None and obj.time_out is not None):
            ti=obj.time_in
            to=obj.time_out
            hours=((to-ti).total_seconds())/3600
            obj.hours=hours

        else:
            obj.hours=0

        (check,break_hourss)= validity_times_check(times_all)
        if check:
            obj.break_hours=break_hourss
        else:
            obj.break_hours=0

        df_hours.append(obj.hours)
        df_break_hours.append(obj.break_hours)
        obj.hours=convert_hours_to_hours_mins(obj.hours)
        obj.break_hours=convert_hours_to_hours_mins(obj.break_hours)

    df = read_frame(qs)
    df["hours"]=df_hours

    print(df)

    sns.barplot(data=df,x='date',y='hours')
    plt.xticks(rotation='vertical')
    rcParams.update({'figure.autolayout': True})
    plt.tight_layout()
    if(admin):
        plt.savefig('./face_in/static/img/attendance_graphs/hours_vs_date/1.png')
        plt.close()
    else:
        plt.savefig('./face_in/static/img/attendance_graphs/user_login/1.png')
        plt.close()
    return qs

#for analytics of a given date
def hours_vs_username_given_date(present_qs,time_qs):
    register_matplotlib_converters()
    df_hours=[]
    df_break_hours=[]
    df_username=[]
    qs=present_qs

    for obj in qs:
        user=obj.user
        times_in=time_qs.filter(user=user).filter(out=False)
        times_out=time_qs.filter(user=user).filter(out=True)
        times_all=time_qs.filter(user=user)
        obj.time_in=None
        obj.time_out=None
        obj.hours=0
        obj.hours=0
        if (len(times_in)>0):			
            obj.time_in=times_in.first().time
        if (len(times_out)>0):
            obj.time_out=times_out.last().time
        if(obj.time_in is not None and obj.time_out is not None):
            ti=obj.time_in
            to=obj.time_out
            hours=((to-ti).total_seconds())/3600
            obj.hours=hours
        else:
            obj.hours=0
        (check,break_hourss)= validity_times_check(times_all)
        if check:
            obj.break_hours=break_hourss
        else:
            obj.break_hours=0   
            
        df_hours.append(obj.hours)
        df_username.append(user.username)
        df_break_hours.append(obj.break_hours)
        obj.hours=convert_hours_to_hours_mins(obj.hours)
        obj.break_hours=convert_hours_to_hours_mins(obj.break_hours)

    df = read_frame(qs)	
    df['hours']=df_hours
    df['username']=df_username
    df["break_hours"]=df_break_hours

    sns.barplot(data=df,x='username',y='hours')
    plt.xticks(rotation='vertical')
    rcParams.update({'figure.autolayout': True})
    plt.tight_layout()
    plt.savefig('./face_in/static/img/attendance_graphs/hours_vs_users/1.png')
    plt.close()
    return qs
    

#Total users registered by the admin     
def total_number_users():
    qs=User.objects.all()
    return (len(qs) -1) # -1 to account for admin 


#Total users present on a given day   
def users_present_count_today():
    today=datetime.date.today()
    qs=Present.objects.filter(date=today).filter(present=True)
    return len(qs)

# Plotting grah of users count this week
def this_week_count():
    today=datetime.date.today()
    some_day_last_week=today-datetime.timedelta(days=7)
    monday_of_last_week=some_day_last_week-  datetime.timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + datetime.timedelta(days=7)
    qs=Present.objects.filter(date__gte=monday_of_this_week).filter(date__lte=today)
    str_dates=[]
    users_count=[]
    str_dates_all=[]
    users_cnt_all=[]
    cnt=0

    for obj in qs:
        date=obj.date
        str_dates.append(str(date))
        qs=Present.objects.filter(date=date).filter(present=True)
        users_count.append(len(qs))
    
    while(cnt<6):
        date=str(monday_of_this_week+datetime.timedelta(days=cnt))
        cnt+=1
        str_dates_all.append(date)
        if(str_dates.count(date))>0:
            idx=str_dates.index(date)
            users_cnt_all.append(users_count[idx])
        else:
            users_cnt_all.append(0)
    
    df=pd.DataFrame()
    df["date"]=str_dates_all
    df["Number of users"]=users_cnt_all  

    sns.lineplot(data=df,x='date',y='Number of users')
    plt.savefig('./face_in/static/img/attendance_graphs/this_week/1.png')
    plt.close()

# Plotting grah of users count last week
def last_week_count():
    today=datetime.date.today()
    some_day_last_week=today-datetime.timedelta(days=7)
    monday_of_last_week=some_day_last_week-  datetime.timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + datetime.timedelta(days=7)
    qs=Present.objects.filter(date__gte=monday_of_last_week).filter(date__lt=monday_of_this_week)
    str_dates=[]
    users_count=[]

    str_dates_all=[]
    users_cnt_all=[]
    cnt=0

    for obj in qs:
        date=obj.date
        str_dates.append(str(date))
        qs=Present.objects.filter(date=date).filter(present=True)
        users_count.append(len(qs))

    while(cnt<6):
        date=str(monday_of_last_week+datetime.timedelta(days=cnt))
        cnt+=1
        str_dates_all.append(date)
        if(str_dates.count(date))>0:
            idx=str_dates.index(date)
            users_cnt_all.append(users_count[idx])           
        else:
            users_cnt_all.append(0)
    
    df=pd.DataFrame()
    df["date"]=str_dates_all
    df["users_count"]=users_cnt_all 

    sns.lineplot(data=df,x='date',y='users_count')
    plt.savefig('./face_in/static/img/attendance_graphs/last_week/1.png')
    plt.close()


# Create your views here.

# Login function
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.username!='admin@facein':
                auth.login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect('dashboard')
            else:
                auth.login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

# Register function
def register(request):     
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                    auth.login(request, user)
                    messages.success(request, 'Registered Successfully!')
                    return redirect('admin_dashboard')
                    user.save()
                    
        else:
            messages.error(request, 'Password do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

# User Dashboard
@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

# Admin Dashboard
def admin_dashboard(request):    
    return render(request, 'accounts/admin_dashboard.html')

# Logout
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return redirect('home')

# Add images Function
@login_required(login_url = 'login')
def add_images(request):
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            dataset_creation(username)
            messages.success(request, 'Images Added Successfully')
            return redirect('admin_dashboard')
            
        else:
            messages.error(request, "Username Doesn't exist! Create Dataset First")
            return redirect('register')
    else:
        return render(request, 'accounts/add_images.html')

# Training Dataset Function
@login_required(login_url = 'login')
def train(request):
 
    training_dir='face_files/face_dataset'

    count=0
    for person_name in os.listdir(training_dir):
        curr_directory=os.path.join(training_dir,person_name)
        if not os.path.isdir(curr_directory):
            continue
        for imagefile in image_files_in_folder(curr_directory):
            count+=1

    X=[]
    y=[]
    i=0

    for person_name in os.listdir(training_dir):
        print(str(person_name))
        curr_directory=os.path.join(training_dir,person_name)
        if not os.path.isdir(curr_directory):
            continue
        for imagefile in image_files_in_folder(curr_directory):
            print(str(imagefile))
            image=cv2.imread(imagefile)
            try:
                X.append((face_recognition.face_encodings(image)[0]).tolist())      
                y.append(person_name)
                i+=1
            except:
                print("Removed")
                os.remove(imagefile)

    targets=np.array(y)
    encoder = LabelEncoder()
    encoder.fit(y)
    y=encoder.transform(y)
    X1=np.array(X)
    print("shape: "+ str(X1.shape))
    np.save('face_files/classes.npy', encoder.classes_)
    svc = SVC(kernel='linear',probability=True)
    svc.fit(X1,y)
    svc_save_path="face_files/svc.sav"
    with open(svc_save_path, 'wb') as f:
        pickle.dump(svc,f)

    Data_vizualization(X1,targets)
    messages.success(request, f'Training Complete.')
    return render(request, "accounts/train.html")
    
# Mark Attendance In
@login_required(login_url = 'login')
def mark_in(request):
    current_user = request.user
    if(current_user.username == 'admin@facein'):
        return redirect('login')

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('face_files/shape_predictor_68_face_landmarks.dat')   
    svc_save_path="face_files/svc.sav"

    with open(svc_save_path, 'rb') as f:
        svc = pickle.load(f)
    fa = FaceAligner(predictor , desiredFaceWidth = 96)
    encoder=LabelEncoder()
    encoder.classes_ = np.load('face_files/classes.npy')

    faces_encodings = np.zeros((1,128))
    no_of_faces = len(svc.predict_proba(faces_encodings)[0])
    count = dict()
    present = dict()
    log_time = dict()
    start = dict()
    for i in range(no_of_faces):
        count[encoder.inverse_transform([i])[0]] = 0
        present[encoder.inverse_transform([i])[0]] = False
    
    vs = VideoStream(src=0).start() 
    sampleNum = 0

    while(True): 
        frame = vs.read()
        frame = imutils.resize(frame ,width = 800)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray_frame,0)
        for face in faces:
            print("INFO : inside for loop")
            (x,y,w,h) = face_utils.rect_to_bb(face)

            face_aligned = fa.align(frame,gray_frame,face)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1) 

            (pred,prob)=prediction(face_aligned,svc)

            if(pred!=[-1]): 
                person_name=encoder.inverse_transform(np.ravel([pred]))[0]
                pred=person_name
                if count[pred] == 0:
                    start[pred] = time.time()
                    count[pred] = count.get(pred,0) + 1
                if count[pred] == 4 and (time.time()-start[pred]) > 1.2:
                     count[pred] = 0
                else:
                    present[pred] = True
                    log_time[pred] = datetime.datetime.now()
                    count[pred] = count.get(pred,0) + 1
                    print(pred, present[pred], count[pred])
                    if(pred!=current_user.username): #More than One Users at a time or using wrong account to mark attendance
                        vs.stop()
                        cv2.destroyAllWindows()
                        messages.success(request, f'Note: One user in a single frame and use your own account for marking attendance!')
                        return render(request, "accounts/dashboard.html")
                    
                cv2.putText(frame, str(person_name)+ str(prob), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)
            else:
                person_name="unknown"
                cv2.putText(frame, str(person_name), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)

        cv2.imshow("Mark Attendance - In - Press p to exit",frame)

        #To get out of the loop
        key=cv2.waitKey(50) & 0xFF
        if(key==ord("p")):
            break

    #Stoping the videostream
    vs.stop()
    
    # destroying all the windows
    cv2.destroyAllWindows()
    
    mark_in_update(present)

    #sending email about the attendance
    email_subject = 'New Message from FaceIn Website Regarding Your Attendance!'
    message_body = 'Dear ' + person_name + ', Your attendance for today has been marked-in. Enjoy your day!'

    email = current_user.email
    send_mail(
        email_subject,
        message_body,
        'noreplyfacein@gmail.com',
        [email],
        fail_silently=False,
    )
    messages.success(request, f'Attendance Marked In and Email Sent Successfully!')
    return render(request, "accounts/dashboard.html")

# Mark Attendance Out
@login_required(login_url = 'login')
def mark_out(request):
    current_user = request.user
    if(current_user.username == 'admin@facein'):
        return redirect('login')
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('face_files/shape_predictor_68_face_landmarks.dat')   #Add path to the shape predictor ######CHANGE TO RELATIVE PATH LATER
    svc_save_path="face_files/svc.sav"

    with open(svc_save_path, 'rb') as f:
        svc = pickle.load(f)
    fa = FaceAligner(predictor , desiredFaceWidth = 96)
    encoder=LabelEncoder()
    encoder.classes_ = np.load('face_files/classes.npy')

    faces_encodings = np.zeros((1,128))
    no_of_faces = len(svc.predict_proba(faces_encodings)[0])
    count = dict()
    present = dict()
    log_time = dict()
    start = dict()
    for i in range(no_of_faces):
        count[encoder.inverse_transform([i])[0]] = 0
        present[encoder.inverse_transform([i])[0]] = False

    vs = VideoStream(src=0).start()
    sampleNum = 0

    while(True):
        frame = vs.read()       
        frame = imutils.resize(frame ,width = 800)   
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        faces = detector(gray_frame,0)

        for face in faces:
            print("INFO : inside for loop")
            (x,y,w,h) = face_utils.rect_to_bb(face)

            face_aligned = fa.align(frame,gray_frame,face)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)

            (pred,prob)=prediction(face_aligned,svc)

            if(pred!=[-1]): 
                person_name=encoder.inverse_transform(np.ravel([pred]))[0]
                pred=person_name
                if count[pred] == 0:
                    start[pred] = time.time()
                    count[pred] = count.get(pred,0) + 1
                if count[pred] == 4 and (time.time()-start[pred]) > 1.5:
                     count[pred] = 0
                else:
                    present[pred] = True
                    log_time[pred] = datetime.datetime.now()
                    count[pred] = count.get(pred,0) + 1
                    print(pred, present[pred], count[pred])
                    if(pred!=current_user.username): #More than One Users at a time or using wrong account to mark attendance
                        vs.stop()
                        cv2.destroyAllWindows()
                        messages.success(request, f'Note: One user in a single frame and use your own account for marking attendance!')
                        return render(request, "accounts/dashboard.html")
                cv2.putText(frame, str(person_name)+ str(prob), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)
            else:
                person_name="unknown"
                cv2.putText(frame, str(person_name), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1) 

        cv2.imshow("Mark Attendance- Out - Press p to exit",frame)

        #To get out of the loop
        key=cv2.waitKey(50) & 0xFF
        if(key==ord("p")):
            break  

    #Stoping the videostream
    vs.stop()
    # destroying all the windows
    cv2.destroyAllWindows()


    mark_out_update(present)
    #sending email about the attendance
    email_subject = 'New Message from FaceIn Website Regarding Your Attendance!'
    message_body = 'Dear ' + person_name + ', Your attendance for today has been marked-out. See you soon again!'

    email = current_user.email
    send_mail(
                email_subject,
                message_body,
                'noreplyfacein@gmail.com',
                [email],
                fail_silently=False,
                )
    messages.success(request, f'Attendance Marked Out and Email Sent Successfully!')
    return render(request, "accounts/dashboard.html")

    
# Analytics for the Admin_Dashboard  
@login_required(login_url = 'login')
def admin_analytics(request):
    current_user = request.user
    if(current_user.username != 'admin@facein'):
        return redirect('login')
    
    total_num_of_users= total_number_users()
    users_present_today=users_present_count_today()
    this_week_count()
    last_week_count()
    data = {
        'total_num_of_users' : total_num_of_users,
        'users_present_today': users_present_today,
    }
    return render(request,"accounts/admin_analytics.html", data)

# Analytics for the User Dashboard
@login_required(login_url = 'login')
def analytics(request):
    current_user = request.user
    if(current_user.username == 'admin@facein'):
        return redirect('login')
    qs=None
    time_qs=None
    present_qs=None

    if request.method=='POST':
        form=DateForm_2(request.POST)
        if form.is_valid():
            u=request.user
            time_qs=Time.objects.filter(user=u)
            present_qs=Present.objects.filter(user=u)
            date_from=form.cleaned_data.get('date_from')
            date_to=form.cleaned_data.get('date_to')
            if date_to < date_from:
                    messages.warning(request, f'Invalid date selection.')
                    return redirect('analytics')

            else:
                time_qs=time_qs.filter(date__gte=date_from).filter(date__lte=date_to).order_by('-date')
                present_qs=present_qs.filter(date__gte=date_from).filter(date__lte=date_to).order_by('-date')
                if (len(time_qs)>0 or len(present_qs)>0):
                    qs=hours_vs_date_username(present_qs,time_qs,admin=False)
                    return render(request,'accounts/analytics.html', {'form' : form, 'qs' :qs})

                else:       
                    messages.warning(request, f'No records for selected duration.')
                    return redirect('analytics')  

    else:
        form=DateForm_2()
        return render(request,'accounts/analytics.html', {'form' : form, 'qs' :qs})


# Search By Date in Admin Analytics
@login_required(login_url = 'login')
def search_by_date(request):
    current_user = request.user
    if(current_user.username != 'admin@facein'):
        return redirect('login')
    qs=None
    time_qs=None
    present_qs=None

    if request.method=='POST':
        form=DateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data.get('date')
            print("date:"+ str(date))
            time_qs=Time.objects.filter(date=date)
            present_qs=Present.objects.filter(date=date)

            if(len(time_qs)>0 or len(present_qs)>0):
                qs=hours_vs_username_given_date(present_qs,time_qs)
                return render(request,'accounts/search_by_date.html', {'form' : form,'qs' : qs })
            else:
                messages.warning(request, f'No records for selected date.')
                return redirect('search_by_date')

    else:
        form=DateForm()
        return render(request,'accounts/search_by_date.html', {'form' : form, 'qs' : qs})

# Search by username in Admin Analytics
@login_required(login_url = 'login')
def search_by_username(request):
    current_user = request.user
    if(current_user.username != 'admin@facein'):
        return redirect('login')
    time_qs=None
    present_qs=None
    qs=None

    if request.method=='POST':
        form=UsernameAndDateForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists(): 

                u=User.objects.get(username=username) 

                time_qs=Time.objects.filter(user=u)
                present_qs=Present.objects.filter(user=u)
                date_from=form.cleaned_data.get('date_from')
                date_to=form.cleaned_data.get('date_to') 

                if date_to < date_from:
                    messages.warning(request, f'Invalid date selection.')
                    return redirect('search_by_username')

                else:
                    time_qs=time_qs.filter(date__gte=date_from).filter(date__lte=date_to).order_by('-date')
                    present_qs=present_qs.filter(date__gte=date_from).filter(date__lte=date_to).order_by('-date')  

                    if (len(time_qs)>0 or len(present_qs)>0):
                        qs=hours_vs_date_username(present_qs,time_qs,admin=True)
                        return render(request,'accounts/search_by_username.html', {'form' : form, 'qs' :qs})

                    else:
                        #print("inside qs is None")
                        messages.warning(request, f'No records for selected duration.')
                        return redirect('search_by_username')             
            else:
                print("invalid username")
                messages.warning(request, f'No such username found.')
                return redirect('search_by_username')
    else:       
        form=UsernameAndDateForm()
        return render(request,'accounts/search_by_username.html', {'form' : form, 'qs' :qs})

@login_required(login_url = 'login') 
def update(request):
    if request.method == 'POST':
        username = request.POST['username']      #Details for which user is to be updated
        if User.objects.filter(username=username).exists():
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']        
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            if password == confirm_password:
                user = User.objects.get(username=username)
                user.username= username
                user.first_name = firstname
                user.last_name = lastname
                user.email = email
                user.password = password
                user.save()
                messages.success(request, 'Information Updated Successfully!')
                return redirect('admin_dashboard')                
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('update')
        else:
            messages.error(request, 'Username doesnot exist!')
            return redirect('update')
    else:
        return render(request, 'accounts/update.html')

    

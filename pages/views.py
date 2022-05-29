from django.shortcuts import render, redirect
from .models import Review
from .models import Feature
from .models import Customer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.

def home(request):
    reviews = Review.objects.all()
    features = Feature.objects.all()
    customers= Customer.objects.all()
    data = {
        'reviews': reviews,
        'features': features,
        'customers': customers,
    }
    return render(request, 'pages/home.html', data)


def about(request):
    reviews = Review.objects.all()
    customers= Customer.objects.all()
    data = {
        'reviews': reviews,
        'customers': customers,
    }
    return render(request, 'pages/about.html', data)

def services(request):
    return render(request, 'pages/services.html')
    

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        phone = request.POST['phone']
        message = request.POST['message']

        email_subject = 'New message from FaceIn website'
        message_body =  name + ' inquired about the ' + subject + '. The details as filled in the contact form are: '+ '1. Name- ' + name + ' 2. Email- ' + email + ' 3. Phone- ' + phone + ' 4. Message- ' + message + ' Please reply as soon as possible. '

        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email
        send_mail(
                email_subject,
                message_body,
                'noreplyfacein@gmail.com',
                [admin_email],
                fail_silently=False,
            )
        messages.success(request, 'Thank you for contacting us. We will get back to you shortly!')
        return redirect('contact')

    return render(request, 'pages/contact.html')

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from  Base import models
from Base.models import Contact
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


def contact(request):
    if request.method=="POST":
        print("post")
        print(request.POST)
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        user_message=request.POST.get('message')
        print(name," ",email," ",subject," ",user_message)

    
        # Validate required fields
        if not name or not email or not subject or not user_message:
            messages.error(request, 'All fields are required!')
            return render(request, 'index.html')

        try:
            # Save the contact form data to the database
            ins = models.Contact(name=name, email=email, subject=subject, messages=user_message)
            ins.save()

             # Send email to your Gmail
            full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{user_message}"
            send_mail(
                subject,
                full_message,
                settings.EMAIL_HOST_USER,  # From email (your Gmail)
                ["your_email@gmail.com"],  # Receiver (your Gmail)
                fail_silently=False,
            )



            messages.success(request, 'Thank You for contacting me! Your message is saved.')
            print('Data has been saved to the database')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            print(f'Error: {str(e)}')

    return render(request,'index.html')
from django.shortcuts import render
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse

# Create your views here.


def ajax_sendmail(request):

    if request.method == 'POST':
        name = request.POST['name']
        subject = request.POST['subject']
        message = request.POST['message']
        from_email = "Jing.Wang@smflc.co.jp"
        recipient_list = [
            request.POST['email']
        ]
        #send_mail(subject, message+" "+name, from_email, recipient_list)
        return HttpResponse('200 OK')

    return HttpResponse('email send failed')
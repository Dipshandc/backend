from django.http import BadHeaderError
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer
from django.core.mail import send_mail
from templated_mail.mail import BaseEmailMessage
from django.conf import settings

class UserRegister(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()
        # Generates confirmation code
        confirmation_code = user.generate_confirmation_code()
        message = BaseEmailMessage(template_name='emails/mail.html',
        context={'user':user.username,'code':confirmation_code})
            
        message.send([user.email])
    

        # subject = 'Confirm your email'
        # message = f'Your confirmation code is: {confirmation_code}'
        # from_email = settings.EMAIL_HOST_USER
        # recipient_list = [user.email]
        # send_mail(subject, message, from_email, recipient_list)

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from . import serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout


from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site

# for generating token
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

# for sending email 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class UserRegistration(APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # confirm_link = f'http://127.0.0.1:8000/accounts/activate/{uid}/{token}/'
            current_site = get_current_site(request)
            confirm_link = f'https://{current_site.domain}/accounts/activate/{uid}/{token}'
            
            email_subject = 'Confirm your email'
            email_body = render_to_string('confirm_email.html',{'confirm_link': confirm_link} )
            email = EmailMultiAlternatives(
                email_subject, '' , to=[user.email]
            )
            email.attach_alternative(email_body, 'text/html')
            email.send()

            return Response('Check your email for activation link')
        return Response(serializer.errors)
        


def activate(request, uid64, token):
    try: 
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk = uid)
    except(User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    


class UserLoginApiView(APIView):

    def post(self,request):
        serializer = serializers.UserLoginSerializer(data = self.request.data)

        if serializer.is_valid():
            username =serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username = username, password = password)

            if user:
                token, _ = Token.objects.get_or_create(user = user)  
                # print(token)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': 'Invalid credentials'})
        return Response(serializer.errors)
    

# give userProfileUpdateView
class UserProfileUpdateView(APIView):

    def get(self, request):
        user = request.user
        serializer = serializers.UserUpdateSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = serializers.UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class UserLogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
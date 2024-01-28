from rest_framework import serializers
from .models import UserDetails
from django.contrib.auth.models import User
GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)



class RegistrationSerializer(serializers.ModelSerializer):

    birth_date = serializers.DateField(write_only=True, input_formats=['%Y-%m-%d'], required=False)
    gender = serializers.ChoiceField(choices=GENDER_TYPE)
    profile_pic = serializers.ImageField(required=False)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name','email', 'password', 'confirm_password', 'birth_date', 'gender', 'profile_pic']

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        # profile_pic = self.validated_data['profile_pic']
        birth_date = self.validated_data['birth_date']
        gender = self.validated_data['gender']
        profile_pic = self.validated_data.get('profile_pic', None)

        if password != password2:
            raise serializers.ValidationError({'error': "Passwords doesn't matched"})
        
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError({'error': "Email already exists"})
        
        account = User(email = email, username = username, first_name = first_name, last_name = last_name)
        account.set_password(password)
        account.is_active = False 
        account.save()

        UserDetails.objects.create(user = account, profile_pic = profile_pic, birth_date = birth_date, gender = gender)

        return account
    


class UserUpdateSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(write_only=True, input_formats=['%Y-%m-%d'], required=False)
    gender = serializers.ChoiceField(choices=GENDER_TYPE)
    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date', 'gender', 'profile_pic']

    def update(self, instance, validated_data):
        user_details_instance, created = UserDetails.objects.get_or_create(user = instance, defaults = {'birth_date': instance.birth_date, 'gender': instance.gender, 'profile_pic': instance.profile_pic})

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        # Update user details fields
        user_details_instance.gender = validated_data.get('gender', user_details_instance.gender)
        user_details_instance.birth_date = validated_data.get('birth_date', user_details_instance.birth_date)
        user_details_instance.profile_pic = validated_data.get('profile_pic', user_details_instance.profile_pic)
        user_details_instance.save()

        return instance

    




class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

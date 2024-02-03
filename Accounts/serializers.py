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
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)



# class UserUpdateSerializer(serializers.ModelSerializer):
#     birth_date = serializers.DateField(write_only=True, input_formats=['%Y-%m-%d'], required=False)
#     gender = serializers.ChoiceField(choices=GENDER_TYPE)
#     profile_pic = serializers.ImageField(required=False)

#     class Meta:
#         model = UserDetails
#         fields = ['username','first_name', 'last_name', 'birth_date', 'gender', 'profile_pic']
    
#     def create(self, validated_data):
#         return UserDetails.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.username = validated_data.get('username', instance.username)
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#         instance.birth_date = validated_data.get('birth_date', instance.address.birth_date)
#         instance.gender = validated_data.get('gender', instance.address.gender)
#         instance.profile_pic = validated_data.get('profile_pic', instance.address.profile_pic)
#         instance.save()
#         return instance
    
# class UserDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserDetails
#         fields = ['birth_date', 'gender', 'profile_pic']

# class UserUpdateSerializer(serializers.ModelSerializer):
#     user_details = UserDetailsSerializer(source='address', read_only=True)

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'user_details']

#     def update(self, instance, validated_data):
#         user_details_data = validated_data.pop('address', {})  # Use the correct related name here

#         # Update User fields
#         instance.username = validated_data.get('username', instance.username)
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
        
#         # Update or create UserDetails
#         user_details_instance, created = UserDetails.objects.get_or_create(user=instance)
#         user_details_serializer = UserDetailsSerializer(user_details_instance, data=user_details_data, partial=True)

#         if user_details_serializer.is_valid():
#             user_details_serializer.save()

#         instance.save()
#         return instance



# class UserDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserDetails
#         fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(write_only=True, input_formats=['%Y-%m-%d'], required=False)
    gender = serializers.ChoiceField(choices=GENDER_TYPE, required=False)
    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date', 'gender', 'profile_pic']

    def update(self, instance, validated_data):
        user_details_data = validated_data.pop('user_details', {})

        # Update User fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update or create UserDetails
        user_details_instance, created = UserDetails.objects.get_or_create(user=instance)

        user_details_instance.gender = user_details_data.get('gender', user_details_instance.gender)
        user_details_instance.birth_date = user_details_data.get('birth_date', user_details_instance.birth_date)
        user_details_instance.profile_pic = user_details_data.get('profile_pic', user_details_instance.profile_pic)
        user_details_instance.save()

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Check if the user has UserDetails related to their account
        if hasattr(instance, 'address'):
            user_details = instance.address
            representation['gender'] = user_details.gender
            representation['birth_date'] = user_details.birth_date
            # representation['profile_pic'] = user_details.profile_pic

        return representation
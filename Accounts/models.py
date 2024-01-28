from django.db import models
from django.contrib.auth.models import User
# Create your models here.
GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

class UserDetails(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='accounts/static/profile_pics/')
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    def __str__(self):
        return str(self.user.email)
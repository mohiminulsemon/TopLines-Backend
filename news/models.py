from django.db import models
from Accounts.models import User
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.ImageField(null=True, blank=True, upload_to='news/static/images/')

    def __str__(self):
        return self.title
    
STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),]

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'ratings')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rating = models.CharField(choices = STAR_CHOICES, max_length = 10)


    def __str__(self):
        return f'{self.post.title} - {self.rating}'
from django.db import models
from users.models import CustomUser

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return str(self.category)
    
class Tag(models.Model):
    tag = models.CharField(max_length=50)

    def __str__(self):
        return str(self.tag)
    
class Blog(models.Model):

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=500)
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="blogs")
    category= models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,related_name="blogs")
    status = models.CharField(choices=STATUS_CHOICES, default='draft')
    blog_content = models.TextField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return str(self.title)

class Comments(models.Model):
    comment = models.TextField()
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="comments")
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return str(self.author) + " " + str(self.blog.title) 

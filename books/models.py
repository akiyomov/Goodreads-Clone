from django.db import models
from users.models import CustomUser
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200) #varchar
    description = models.TextField()
    isbn = models.CharField(max_length=17)
    cover_picture = models.ImageField(default='default_cover_image.jpg')

    def __str__(self):
        return self.title



class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    def __str__(self):
        return f"{self.first_name} {self.last_name} "

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.book.title} by {self.author.first_name} {self.author.last_name}"
    


class BookReview(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    comment = models.TextField()
    stars_given = models.IntegerField(
        validators = [MinValueValidator(1),MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.stars_given} for '{self.book.title}' by {self.user.username}"
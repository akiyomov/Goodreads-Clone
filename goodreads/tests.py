from django.test import TestCase
from users.models import CustomUser
from books.models import BookReview,Book
from django.urls import reverse 

class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='Book1',description='Description',isbn='12345678910')
        user = CustomUser.objects.create(username="anvar",first_name="Anvar",last_name="Kiyomov",email="anvar@gmail.com")
        user.set_password("asad")
        user.save()     
        self.client.login(username="anvar",password="asad")
        review1 = BookReview.objects.create(user=user,book=book,stars_given=3,comment="Nice book")
        review2 = BookReview.objects.create(user=user,book=book,stars_given=4,comment="Good book")
        review3 = BookReview.objects.create(user=user,book=book,stars_given=5,comment="Very good book")

        response = self.client.get(reverse('home_page') + '?page_size=2')
        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)

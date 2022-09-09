from django.test import TestCase
from django.urls import reverse
from books.models import Book,Author,BookAuthor
from users.models import CustomUser
# Create your tests here.

class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('list'))



        self.assertContains(response,"No books found.")


    def test_books_list(self):
        book1 = Book.objects.create(title='Book1',description='Description',isbn='12345678910')
        book2 = Book.objects.create(title='Book2',description='Description2',isbn='12345678990')
        book3 = Book.objects.create(title='Book3',description='Description3',isbn='12345678911')

        response = self.client.get(reverse('list')+"?page_size=2")

        books = Book.objects.all()
        for book in [book1,book2]:
            self.assertContains(response,book.title)
        self.assertNotContains(response, book3.title)
        response = self.client.get(reverse('list') + "?page=2&page_size=2")
        self.assertContains(response, book3.title )
    def test_detail_page(self):
        book = Book.objects.create(title="Book",description="Description",isbn="109876543210")
        author = Author.objects.create(first_name="Asadbek",last_name="Kiyomov",email="asad@gmail.com",bio="ZFake")
        book_author = BookAuthor.objects.create(book=book,author=author)
        response = self.client.get(reverse('detail',kwargs={"id":book.id}))

        
        self.assertContains(response,book.title)
        self.assertContains(response,book.description)
        self.assertTrue(book_author)

    def test_search_books(self):
        book1 = Book.objects.create(title='Sport',description='Description',isbn='12345678910')
        book2 = Book.objects.create(title='Education',description='Description2',isbn='12345678990')
        book3 = Book.objects.create(title='Test',description='Description3',isbn='12345678911')
        response = self.client.get(reverse('list') + "?q=sport")
        self.assertContains(response,book1.title)
        self.assertNotContains(response,book2.title)
        self.assertNotContains(response,book3.title)

        response = self.client.get(reverse('list') + "?q=education")
        self.assertContains(response,book2.title)
        self.assertNotContains(response,book1.title)
        self.assertNotContains(response,book3.title)

        response = self.client.get(reverse('list') + "?q=Test")
        self.assertContains(response,book3.title)
        self.assertNotContains(response,book2.title)
        self.assertNotContains(response,book1.title)

class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title='Sport',description='Description',isbn='12345678910')
        user = CustomUser.objects.create(username="anvar",first_name="Anvar",last_name="Kiyomov",email="anvar@gmail.com")
        user.set_password("asad")
        user.save()     

        self.client.login(username="anvar",password="asad")
        self.client.post(reverse('reviews',kwargs={'id':book.id}),data={
            'stars_given' : 3,
            'comment':'ice book'
        }
        )
        book_reviews = book.bookreview_set.all()
        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].user, user)
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, 'ice book')



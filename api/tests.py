from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from books.models import Book,BookReview
from users.models import CustomUser
# Create your tests here.
class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="asad",first_name="Asadbek")
        self.user.set_password("asad")
        self.user.save()
        self.client.login(username="asad",password="asad")

    def test_book_review_detail(self):
        book = Book.objects.create(title="Book", description="Description",isbn="123456")
        br = BookReview.objects.create(book=book, user=self.user,comment="nice",stars_given=5)

        response = self.client.get(reverse('api:review-detail',kwargs={"id":br.id}))
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['id'],br.id)
        self.assertEqual(response.data['comment'],br.comment)
        self.assertEqual(response.data['stars_given'],br.stars_given)
        self.assertEqual(response.data['book']['id'],br.book.id)
        self.assertEqual(response.data['book']['title'],br.book.title)
        self.assertEqual(response.data['book']['isbn'],br.book.isbn)
        self.assertEqual(response.data['book']['description'],'Description')
        self.assertEqual(response.data['user']['id'],br.user.id)
        self.assertEqual(response.data['user']['first_name'],br.user.first_name)
        self.assertEqual(response.data['user']['username'],'asad')


    def test_delete_review(self):
        book = Book.objects.create(title="Book", description="Description",isbn="123456")
        br = BookReview.objects.create(book=book, user=self.user,comment="nice",stars_given=5)
        response = self.client.delete(reverse('api:review-detail',kwargs={"id":br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())

    def test_update_review(self):
        book = Book.objects.create(title="Book", description="Description",isbn="123456")
        br = BookReview.objects.create(book=book, user=self.user,comment="nice",stars_given=5)
        response = self.client.patch(reverse('api:review-detail',kwargs={"id":br.id}),data={'stars_given':1})
        br.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given,1)

    def test_put_review(self):
        book = Book.objects.create(title="Book", description="Description",isbn="123456")
        br = BookReview.objects.create(book=book, user=self.user,comment="nice",stars_given=5)
        response = self.client.patch(
            reverse('api:review-detail',kwargs={"id":br.id}),
            data={'stars_given':2,'comment':"Good job",'book_id':book.id,'user_id':self.user.id})
        br.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 2)
        self.assertEqual(br.comment, 'Good job')
    def test_patch_review(self):
        book = Book.objects.create(title="Book", description="Description",isbn="123456")
        data = {
            'stars_given':5,
            'comment':'Bad book',
            'user_id': self.user.id,
            'book_id':book.id
        }

        response = self.client.post(reverse('api:review-list'),data=data)
        br = BookReview.objects.get(book=book)
        self.assertEqual(response.status_code,201)
        self.assertEqual(br.stars_given,5)
        self.assertEqual(br.comment,'Bad book')

    def test_book_list(self):
        book = Book.objects.create(title="Book", description="Description",isbn="123456")
        user2 = CustomUser.objects.create(username="anvar",first_name="Anvar")
        br = BookReview.objects.create(book=book, user=self.user,comment="nice",stars_given=5)
        br2 = BookReview.objects.create(book=book, user=user2,comment="bad",stars_given=53)
        
        response = self.client.get(reverse('api:review-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']),2)
        self.assertIn('next',response.data)
        self.assertIn('previous',response.data)
        self.assertEqual(response.data['results'][1]['id'],br.id )
        self.assertEqual(response.data['results'][1]['stars_given'],br.stars_given )
        self.assertEqual(response.data['results'][1]['comment'],br.comment )
        self.assertEqual(response.data['results'][0]['id'],br2.id )
        self.assertEqual(response.data['results'][0]['stars_given'],br2.stars_given )
        self.assertEqual(response.data['results'][0]['comment'], br2.comment)
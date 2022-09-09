from django.test import TestCase
from django.contrib import messages
from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth import get_user

# Create your tests here.

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(reverse('users:register'),data={
            "username":"asadbey5",
            "first_name":"Asadbek",
            "last_name":"Kiyamov",
            "email":"asadbek@gmail.com",
            "password":"somepassword"
            })

        user = CustomUser.objects.get(username="asadbey5")
        

        self.assertEqual(user.first_name,"Asadbek")
        self.assertEqual(user.last_name,"Kiyamov")
        self.assertEqual(user.email,"asadbek@gmail.com")
        self.assertNotEqual(user.password,"somepassword")
        self.assertTrue(user.check_password('somepassword'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                "first_name":"Asadbek",
                "email":"asadbek@gmail.com"
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form","username", "This field is required.")
        #self.assertFormError(response, "form", "password", "This field is required.")
    def test_invalid_email(self):
        response = self.client.post(reverse('users:register'),data={
            "username":"asadbey5",
            "first_name":"Asadbek",
            "last_name":"Kiyamov",
            "email":"asadbek",
            "password":"somepassword"
            })
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response,"form","email","Enter a valid email address.")

    def test_unique_username(self):
        #create user
        user = CustomUser.objects.create(username='mohirdev',first_name='uzbekistan')
        user.set_password('newhome')
        user.save()
        response = self.client.post(reverse('users:register'),data={
            "username":"mohirdev",
            "first_name":"uzbekistan",
            
            "password":"somepassword"
            })

        user_exists = CustomUser.objects.count()
        self.assertEqual(user_exists, 1)
        self.assertFormError(response,"form","username","A user with that username already exists.")

class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username="asad",first_name="")
        self.db_user.set_password("asad")
        self.db_user.save()
    def test_successful_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                "username":"asad",
                "password":"asad"
            }
        )
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('users:login'),
            data={
                "username":"asad",
                "password":"asadss"
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


    def test_logout(self):
        self.client.login(username="asad",password="asad")
        
        self.client.get(reverse('users:logout'))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code,302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")        

    def test_profile_details(self):
        user = CustomUser.objects.create(username="anvar",first_name="Anvar",last_name="Kiyomov",email="anvar@gmail.com")
        user.set_password("asad")
        user.save()     

        self.client.login(username="anvar",password="asad")
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code,200)
        self.assertContains(response,user.username)
        self.assertContains(response,user.first_name)
        self.assertContains(response,user.last_name)
        self.assertContains(response,user.email)

    def test_update_profile(self):
        db_user = CustomUser.objects.create(username="asad",first_name="")
        db_user.set_password("asad")
        db_user.save()

        self.client.login(username="asad",password="asad")
        response = self.client.post(
            reverse('users:profile-edit'),
            data ={
                "username":"asad",
                "first_name":"Asadbey",
                "last_name":"Adam05",
                "email":"adam@net.com"
            } 
            )
        db_user.refresh_from_db()         #User.objects.get(pk=db_user.pk)
        self.assertEqual(db_user.first_name , "Asadbey")
        self.assertEqual(db_user.last_name , "Adam05")
        self.assertEqual(db_user.email, "adam@net.com")
        self.assertEqual(response.url,reverse('users:profile'))





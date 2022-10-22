from django.test import Client, TestCase
from django.shortcuts import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import cragRoute
# from unittest.mock import  patch, MagicMock
# import jsons
from .views import Crags1
# import urllib
import urllib.request
# import io
from .models import userProfile
from math import log

testClient = Client()

dummyTestUsername = "user"
dummyTestPassword = "password"
dummyTestemail = "user@example.com"

def create_user():
    try:
        user = User.objects.create_user(username=dummyTestUsername, email=dummyTestemail,password=dummyTestPassword)
        profile = userProfile()
        profile.userID = user
        profile.save()
    except:
        pass

def cleanup():
    try:
        user = User.objects.get_by_natural_key(dummyTestUsername)
        if not (user is None):
            profile = userProfile.objects.get(userID=user)
            if not (profile is None):
                profile.delete()
            user.delete()
    except:
        pass


# class t1_AuthenticationTests(TestCase):
#     userDetails  = {
#         'username':'testUser',
#         'email':'testUser@test.com',
#         'password1':'password',
#         'password2':'password'
#     }
#     def test1_SignUp(self):
#         print("\nTesting SignUp:")
#         response = testClient.post('/signUp', self.userDetails)
#         print("SignUp status code: ", response.status_code)
#         self.assertEquals(response.status_code, 200)
#     def test2_SignIn(self):
#         print("\nTesting SignIn:")
#         response = testClient.post('/signIn',{ 'username':self.userDetails['username'], 'password':self.userDetails['password1']})
#         print("SignIn status code: ", response.status_code)
#         self.assertEquals(response.status_code, 200)

# class t2_URLTests(TestCase):
#     testURLs = ['','index', 'home','Crags','MyClimbs','MyCommunity','Settings']
#     def test1_URLs(self):
#         for x in self.testURLs:
#             print('\n\ntesting URL:/'+ x)
#             response = testClient.get("/"+x)
#             self.assertIn(response.status_code, [200,302])
#             print('SUCCESS')

# class indexViewTest(TestCase):

#     def test_should_land_user_to_landing_page(self):

#         print("\nTesting indexView while requesting by '/':")

#         response = testClient.get('/')
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, "index.html")
    
#         print("SUCCESS")

#     def test_should_land_user_to_sign_in_page_while_calling_by_index(self):

#         print("\nTesting indexView while requesting by '/index':")

#         response = testClient.get(reverse('index'))
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, "index.html")

#         print("SUCCESS")

class homeViewTest(TestCase):
    
    def test_should_redirect_anonymous_user_to_signin_page(self):

        print("\nTesting that anonymous user is redirected to signin page when requesting home")

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

        print("SUCCESS")

    def test_should_give_access_to_home_page(self):

        print("\nTesting that authenticated user can access home page")

        create_user()

        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        cleanup()

        print("SUCCESS")

# class signInViewTest(TestCase):
    
#     def test_should_return_signIn_page_for_unauthenticated_user_while_doing_get_request(self):

#         print("\nTesting that all users can access signin page")

#         response = self.client.get(reverse('signIn'))
#         print("response", response)
#         self.assertEqual(response.status_code, 200)

#         print("SUCCESS")

#     def test_should_redirect_already_authenticated_users_to_home_page(self):

#         print("\nTesting that authenticated user are redirected to home page")

#         create_user()

#         self.client.login(username=dummyTestUsername, password=dummyTestPassword)
#         response = self.client.get(reverse('signIn'))
#         print("Response", response)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/home')

#         cleanup()

#         print("SUCCESS")

#     def test_should_redirect_authenticated_users_to_home_page(self):

#         print("\nTesting that users who submits valid credential are redirected to home page")

#         create_user()

#         response = self.client.post('/signIn',{ 'username':dummyTestUsername, 'password':dummyTestPassword})
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/home')

#         cleanup()

#         print("SUCCESS")

#     def test_should_return_user_to_sigin_page(self):

#         print("\nTesting that users who submits invalid credential are returned back to signin page")

#         create_user()

#         response = self.client.post('/signIn',{ 'username':dummyTestUsername, 'password':"wrongPassword"})

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'signIn.html')
#         cleanup()

#         print("SUCCESS")

class signUpViewTest(TestCase):
    
    def test_should_redirect_already_authenticated_users_to_home_page(self):
        print('\ntesting that authenticated users are redicted to homepage while doing get request to signUP')

        create_user()

        self.client.login(username=dummyTestUsername, password=dummyTestPassword)

        response = self.client.get(reverse('signUp'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home')
        cleanup()

        print("SUCCESS")

    def test_should_show_signUp_page_to_unauthenticated_user(self):

        print("\nTesting that all users can access sign up page")

        response = self.client.get(reverse('signUp'))
        print("response", response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signUp.html")
        cleanup()
        print("SUCCESS")


    def test_should_return_user_to_signUp_page(self):

        userDetails  = {
          'username':'testUser',
          'email':'testUser@test.com',
          'password1':'password',
        }

        print('\nTesting that users who submit invalid information are returned back to sign Up page')
 
        response = self.client.post("/signUp", userDetails)
        print("response", response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signUp.html")
        cleanup()
        print("SUCCESS")


    def test_should_return_new_user_to_signIn_page(self):

        userDetails  = {
          'username':'ak',
          'email':'ak@test.com',
          'password1':'ak9784@123#%^&',
          'password2':'ak9784@123#%^&'
        }

        print('\nTesting that users who submit valid information are returned back to sign In page')
 
        response = self.client.post("/signUp", userDetails)
        print("response", response)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/signIn")
        print("SUCCESS")


class cragsViewTest(TestCase):

    def test_should_redirect_anonymous_user_to_signin_page(self):

        print("\nTesting that anonymous user is redirected to signin page when requesting Crags")

        response = self.client.get(reverse('Crags'))
        self.assertEqual(response.status_code, 302)

        print("SUCCESS")

    def test_should_give_access_to_crag_page(self):

        print("\nTesting that authenticated user can access crag page")

        create_user()

        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        response = self.client.get(reverse('Crags'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Crags.html')

        cleanup()

        print("SUCCESS")

class Craig1Test(TestCase):
    
    def test_should_redirect_anonymous_user_to_signin_page(self):
        # self.client.login(username="user", password="password")
        print("\nTesting that anonymous user is redirected to signin page when requesting crag1")
        response = self.client.get(reverse('Crags1'))
        self.assertEqual(response.status_code, 302)
        cleanup()
        print("SUCCESS")

    def test_should_return_data_for_logged_in_user(self):
        print("\nTesting that authenticated user receives weather data")
       
        create_user()
        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        response = self.client.get(reverse('Crags1'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Crags1.html')
        cleanup()
        print("SUCCESS")


class Crags2Test(TestCase):

    def test_should_redirect_anonymous_user_to_signin_page(self):
        # self.client.login(username="user", password="password")
        print("\nTesting that anonymous user is redirected to signin page when requesting crag2")
        response = self.client.get(reverse('Crags2'))
        self.assertEqual(response.status_code, 302)
        print("Success")

    def test_should_give_access_to_logged_in_user(self):
        print("\nTesting that authenticated user can access crag2 page")

        create_user()
        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        
        response = self.client.get(reverse('Crags2'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Crags2.html')
        cleanup()
        print("SUCCESS")

    def test_should_redirect_user_Crags_view_when_requesting(self):
        print("\nTesting that authenticated users redirected to Crags3.html view when requesting Crags2 with valid parameters")

        create_user()
        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        
        response = self.client.get(reverse('Crags2') + '?Rating=2&Grade=15&Rope Length=False')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Crags3.html')
        cleanup()
        print("SUCCESS")


class Crags3Test(TestCase):

    def test_should_redirect_anonymous_user_to_signin_page(self):

        print("\nTesting that anonymous user is redirected to signin page when requesting Crags3")

        response = self.client.get(reverse('Crags3'))
        self.assertEqual(response.status_code, 302)

        print("SUCCESS")

    def test_should_give_access_to_crags3_page(self):

        print("\nTesting that authenticated user can access crags3 page")

        create_user()

        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        response = self.client.get(reverse('Crags3'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Crags3.html')

        cleanup()

        print("SUCCESS")

class Crags4Test(TestCase):

    def testing_that_all_users_can_access_Crags4(self):
        print("\nTesting that all users can access Crags4 page")

        response = self.client.get(reverse('Crags4'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Crags4.html")
        print("SUCCESS")

class Crag5Test(TestCase):
    
    def test_should_redirect_anonymous_user_to_signin_page(self):
        # self.client.login(username="user", password="password")
        print("\nTesting that anonymous user is redirected to signin page when requesting crag5")
        response = self.client.get(reverse('Crags5'))
        self.assertEqual(response.status_code, 302)
        print("Success")

    def test_should_give_access_to_logged_in_user(self):
        print("\nTesting that authenticated user can access crag5 page")

        create_user()
        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        
        response = self.client.get(reverse('Crags5'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Crags5.html')
        cleanup()
        print("SUCCESS")

    def test_should_not_update_user_level(self):
        print("\nTesting that when parameters not equal to 2 (grade and rating), it does not update user level")

        create_user()
        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        user = User.objects.get_by_natural_key(dummyTestUsername)
        prevProfile = userProfile.objects.get(userID=user)
        prevLevel = prevProfile.level
        print("Previous level: ", prevLevel)
        response = self.client.get(reverse('Crags5') + '?grade=3')

        currentProfile = userProfile.objects.get(userID=user)
        currentLevel = currentProfile.level
        print("Current level: ", currentLevel)

        self.assertEqual(prevLevel, currentLevel)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Crags5.html')
        cleanup()
        print("SUCCESS")

    def test_should_update_user_level(self):
        print("\nTesting that when parameters equal to 2 (grade and rating), it should update user level")

        create_user()
        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        user = User.objects.get_by_natural_key(dummyTestUsername)

        prevProfile = userProfile.objects.get(userID=user)
        prevLevel = prevProfile.level
        print("prevLevel: ", prevLevel)

        response = self.client.get(reverse('Crags5') + '?grade=3&rating=3')

        currentProfile = userProfile.objects.get(userID=user)
        currentLevel = currentProfile.level
        print("currentLevel: ", currentLevel)

        self.assertEqual(int(log(3*3)) + prevLevel, int(currentLevel))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Crags5.html')
        cleanup()
        print("SUCCESS")

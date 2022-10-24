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
from .models import MBPost
from .models import MBPostLikeStatus
import datetime
from math import log

#Method to test the URLs for every page 
class URLTests(TestCase):
    testURLs = ['','index', 'home','Crags','MyClimbs','MyCommunity','Settings']
    def test1_URLs(self):
        for x in self.testURLs:
            print('\n\ntesting URL:/'+ x)
            response = testClient.get("/"+x)
            self.assertIn(response.status_code, [200,302])
            print('SUCCESS')



testClient = Client()

dummyTestUsername = "user"
dummyTestPassword = "password"
dummyTestemail = "user@example.com"


#Method to create dummy user in the test database
def create_user():
    try:
        user = User.objects.create_user(username=dummyTestUsername, email=dummyTestemail,password=dummyTestPassword)
        profile = userProfile()
        profile.userID = user
        profile.save()
    except:
        pass

#Method to delete the created user from test database
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

#Method to create a dummy post in the test database and return the post object
def create_post(user):
    try:
        message = "Test Message"
        title = "Test Title"
        time = datetime.datetime.now()
        NewPost = MBPost.objects.create(text=message, title=title, time=time, FKUserProfile=userProfile.objects.get(userID=user))
        return NewPost
    except:
        return False

#Method to delete the created post from test database
def cleanupPost():
    try:
        posts = MBPost.objects.all().order_by('-time')
        for post in posts:
            if not (post is None):
                print("Cleaning Dummy Post", post)
                post.delete()
    except:
        pass


#Test case for index view 
class indexViewTest(TestCase):


    #Method to test if "/" lands users to index page 
    def test_should_land_user_to_landing_page(self):

        print("\nTesting indexView while requesting by '/':")

        response = testClient.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
    
        print("SUCCESS")


    #Method to test if "index" lands users to index page 
    def test_should_land_user_to_sign_in_page_while_calling_by_index(self):

        print("\nTesting indexView while requesting by '/index':")

        response = testClient.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

        print("SUCCESS")



#Test case for home view 
class homeViewTest(TestCase):
    

    #Method to test if anonymous user is redirected to signin page when requesting home
    def test_should_redirect_anonymous_user_to_signin_page(self):

        print("\nTesting that anonymous user is redirected to signin page when requesting home")

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

        print("SUCCESS")


    #Method to test if authenticated user can access home page
    def test_should_give_authenticated_users_access_to_home_page(self):

        print("\nTesting that authenticated user can access home page")

        create_user()

        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        cleanup()

        print("SUCCESS")


#Test case for Sign In View
class signInViewTest(TestCase):

    #Method to test if all users can access signin page 
      def test_should_return_signIn_page_for_unauthenticated_user_while_doing_get_request(self):

          print("\nTesting that all users can access signin page")

          response = self.client.get(reverse('signIn'))
          print("response", response)
          self.assertEqual(response.status_code, 200)

          print("SUCCESS")


    #Method to test if authenticated user are redirected to home page
      def test_should_redirect_already_authenticated_users_to_home_page(self):

          print("\nTesting that authenticated user are redirected to home page")

          create_user()

          self.client.login(username=dummyTestUsername, password=dummyTestPassword)
          response = self.client.get(reverse('signIn'))
          print("Response", response)
          self.assertEqual(response.status_code, 302)
          self.assertEqual(response.url, '/home')

          cleanup()

          print("SUCCESS")


    #Method to test if users who submits valid credential are redirected to home page
      def test_should_redirect_authenticated_users_to_home_page(self):

          print("\nTesting that users who submits valid credential are redirected to home page")

          create_user()

          response = self.client.post('/signIn',{ 'username':dummyTestUsername, 'password':dummyTestPassword})
          self.assertEqual(response.status_code, 302)
          self.assertEqual(response.url, '/home')

          cleanup()

          print("SUCCESS")


    #Method to test if users who submits invalid credential are returned back to signin page
      def test_should_return_user_to_sigin_page(self):

          print("\nTesting that users who submits invalid credential are returned back to signin page")

          create_user()

          response = self.client.post('/signIn',{ 'username':dummyTestUsername, 'password':"wrongPassword"})

          self.assertEqual(response.status_code, 200)
          self.assertTemplateUsed(response, 'signIn.html')
          cleanup()

          print("SUCCESS")



#Test case for Sign up view
class signUpViewTest(TestCase):


    #Method to test if authenticated users are redicted to homepage while doing get request to signUP
    def test_should_redirect_already_authenticated_users_to_home_page(self):
        print('\ntesting that authenticated users are redicted to homepage while doing get request to signUP')

        create_user()

        self.client.login(username=dummyTestUsername, password=dummyTestPassword)

        response = self.client.get(reverse('signUp'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/home')
        cleanup()

        print("SUCCESS")


    #Method to test if all users can access sign up page
    def test_should_show_signUp_page_to_unauthenticated_user(self):

        print("\nTesting that all users can access sign up page")

        response = self.client.get(reverse('signUp'))
        print("response", response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signUp.html")
        cleanup()
        print("SUCCESS")


    #Method to test if users who submit invalid information are returned back to sign Up page
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


    #Method to test if users who submit valid information are returned back to sign In page
    def test_should_return_new_user_to_signIn_page(self):

        userDetails  = {
          'username':'Mosammat',
          'email':'ms@test.com',
          'password1':'ms9784@123#%^&',
          'password2':'ms9784@123#%^&'
        }

        print('\nTesting that users who submit valid information are returned back to sign In page')

        response = self.client.post("/signUp", userDetails)
        print("response", response)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/signIn")
        print("SUCCESS")



#Test case for Crags View 
class cragsViewTest(TestCase):


    #Method to test if anonymous user is redirected to signin page when requesting Crags page
    def test_should_redirect_anonymous_user_to_signin_page(self):

        print("\nTesting that anonymous user is redirected to signin page when requesting Crags")

        response = self.client.get(reverse('Crags'))
        self.assertEqual(response.status_code, 302)

        print("SUCCESS")



    #Method to test if authenticated user can access crag page
    def test_should_give_authenticated_user_access_to_crag_page(self):

        print("\nTesting that authenticated user can access crag page")

        create_user()

        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        response = self.client.get(reverse('Crags'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Crags.html')

        cleanup()

        print("SUCCESS")



#Test case for MyClimbs View 
class MyClimbsViewTest(TestCase):

    #Method to test if anonymous user is redirected to signin page when requesting MyClimbs page
    def test_should_redirect_anonymous_user_to_signin_page(self):

        print("\nTesting that anonymous user is redirected to signin page when requesting MyClimbs")

        response = self.client.get(reverse('MyClimbs'))
        self.assertEqual(response.status_code, 302)

        print("SUCCESS")


    #Method to test if authenticated user can access MyClimbs page
    def test_should_give_authenticated_user_access_to_myCommunity_page(self):

        print("\nTesting that authenticated user can access MyClimbs page")

        create_user()

        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        response = self.client.get(reverse('MyClimbs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'MyClimbs.html')

        cleanup()

        print("SUCCESS")



#Test case for MyCommunity View 
class myCommunityViewTest(TestCase):

    #Method to test if anonymous user is redirected to signin page when requesting MyCommunity page
    def test_should_redirect_anonymous_user_to_signin_page(self):

        print("\nTesting that anonymous user is redirected to signin page when requesting myCommunity")

        response = self.client.get(reverse('MyCommunity'))
        self.assertEqual(response.status_code, 302)

        print("SUCCESS")


    #Method to test if authenticated user can access MyCommunity page
    def test_should_give_access_to_myCommunity_page(self):

        print("\nTesting that authenticated user can access myCommunity page")

        create_user()

        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        response = self.client.get(reverse('MyCommunity'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'MyCommunity.html')

        cleanup()

        print("SUCCESS")
    

    #Method to test if authenticated user can create a new post 
    def test_should_create_new_post(self):
        
        print("\nTesting that authenticated user can create new post")

        #Fetching the oldPost Object and Storing it in a variable
        oldPosts = MBPost.objects.all().order_by('-time')
        oldPostCount = oldPosts.count()
        #Printing the oldPost Object and number of posts
        print("oldPosts", oldPosts, oldPosts.count())

        create_user()
        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        #Here user is authenticated and is creating a new post

        #Requesting with post data to Create a new post
        response = self.client.post('/MyCommunity',{'message':'testPost', 'title':'testTitle'})

        #Fetching the newPosts Object and Storing it in a variable
        newPosts = MBPost.objects.all().order_by('-time')

        #Printing the newPosts information
        print("newPosts ID:", newPosts.first().id, "New Post Title: ", newPosts.first().title, "New Post Text :",  newPosts.first().text, newPosts.first().time, newPosts.count())
        
       

        #Checking if the number of posts has increased
        #new post count should be greater than old post count
        self.assertGreater(newPosts.count(), oldPostCount)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'MyCommunity.html')
        cleanupPost()
        cleanup()
        
        print("SUCCESS")



#Test case for likePost View 
class likePostViewTest(TestCase):

    #Method to test if anonymous user is redirected to signin page when requesting likePost
    def test_should_redirect_anonymous_user_to_signin_page(self):

        print("\nTesting that anonymous user is redirected to signin page when requesting likePost")

        response = self.client.get(reverse('likePost'))
        self.assertEqual(response.status_code, 302)

        print("SUCCESS")



    # Method to check if the liked status is added to the post and it a user likes it (is True)

    #The user did not like the post before 
    def test_should_add_the_like_status_for_given_post_id_to_true(self):

        print("\nTesting that authenticated user can like a post")

        create_user()

        # Store the user for later use
        user = User.objects.get_by_natural_key(dummyTestUsername)

        #login using the created user credenrial
        self.client.login(username=dummyTestUsername, password=dummyTestPassword)

        #Create a post for the the logged in user 
        MBCreatedPost = create_post(user)

        #We will pass this post id while requesting likePost
        oldPostID = MBCreatedPost.id

        #Requesting with post id to like the post
        response = self.client.get(reverse('likePost') + '?id='+str(oldPostID))

        #Fetching the new post like status Object and Storing it in a variable
        newPostLikeStatus = MBPostLikeStatus.objects.get(  
            FKUserProfile = userProfile.objects.get(userID=user), 
            FKMBPost = MBCreatedPost)

        # New isLiked status should be true
        self.assertTrue(newPostLikeStatus.isLiked)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/MyCommunity')

        cleanupPost()
        cleanup()
        print("SUCCESS")
    


    # Method to check if the liked status is changed for the post from True to False
    # The User liked this post earlier and now user is unliking the post

    def test_should_update_like_status_for_given_post_id_to_false(self):

        print("\nTesting that authenticated user can unlike a post")

        create_user()

        # Store the user for later use
        user = User.objects.get_by_natural_key(dummyTestUsername)

        #login using the created user credential
        self.client.login(username=dummyTestUsername, password=dummyTestPassword)

        #Create a post for the the logged in user 
        MBCreatedPost = create_post(user)

        #We will pass this post id while requesting likePost
        oldPostID = MBCreatedPost.id

        # Here we are making the created post liked by the user before checking the unlike functionality works or not
        postLikeStatus = MBPostLikeStatus(
            FKUserProfile = userProfile.objects.get(userID=user), 
            FKMBPost = MBCreatedPost, isLiked = True)
        postLikeStatus.save()

        #Requesting with post id to unlike the post
        response = self.client.get(reverse('likePost') + '?id='+str(oldPostID))

        #Fetching the new post like status Object and Storing it in a variable
        newPostLikeStatus = MBPostLikeStatus.objects.get(  
            FKUserProfile = userProfile.objects.get(userID=user), 
            FKMBPost = MBCreatedPost)

        # New isLiked status should be false
        self.assertFalse(newPostLikeStatus.isLiked)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/MyCommunity')

        cleanupPost()
        cleanup()
        print("SUCCESS")


    # Method to check if the liked status is changed for the post from False to True
    # The scenerio is User liked this post earlier and then unliked it and now user is liking the post again
    def test_should_update_like_status_for_given_post_id_from_false_to_true(self):
            
            print("\nTesting that authenticated user can like a post that was unliked earliar")
    
            create_user()
    
            # Store the user for later use
            user = User.objects.get_by_natural_key(dummyTestUsername)
    
            #login using the created user credenrial
            self.client.login(username=dummyTestUsername, password=dummyTestPassword)
    
            #Create a post for the the logged in user 
            MBCreatedPost = create_post(user)
    
            #We will pass this post id while requesting likePost
            oldPostID = MBCreatedPost.id
    
            # Here we are making the created post unliked by the user before checking the like functionality works or not
            postLikeStatus = MBPostLikeStatus(
                FKUserProfile = userProfile.objects.get(userID=user), 
                FKMBPost = MBCreatedPost, isLiked = False)
            postLikeStatus.save()
    
            #Requesting with post id to unlike the post
            response = self.client.get(reverse('likePost') + '?id='+str(oldPostID))
    
            #Fetching the new post like status Object and Storing it in a variable
            newPostLikeStatus = MBPostLikeStatus.objects.get(  
                FKUserProfile = userProfile.objects.get(userID=user), 
                FKMBPost = MBCreatedPost)
    
            # New isLiked status should be true
            self.assertTrue(newPostLikeStatus.isLiked)
    
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/MyCommunity')
    
            cleanupPost()
            cleanup()
            print("SUCCESS")



#Test case for Settings View 
class SettingsViewTest(TestCase):

    #Method to test if anonymous user is redirected to signin page when requesting Settings page
    def test_should_redirect_anonymous_user_to_signin_page(self):

        print("\nTesting that anonymous user is redirected to signin page when requesting Settings")

        response = self.client.get(reverse('Settings'))
        self.assertEqual(response.status_code, 302)

        print("SUCCESS")


    #Method to test if authenticated user can access Settings page
    def test_should_give_authenticated_user_access_to_Settings_page(self):

        print("\nTesting that authenticated user can access Settings page")

        create_user()

        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        response = self.client.get(reverse('Settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Settings.html')

        cleanup()

        print("SUCCESS")



#Test case for Crags1 
class Crag1Test(TestCase):
    
    #Method to test if anonymous user is redirected to signin page when requesting crag1
    def test_should_redirect_anonymous_user_to_signin_page(self):
        # self.client.login(username="user", password="password")
        print("\nTesting that anonymous user is redirected to signin page when requesting crag1")
        response = self.client.get(reverse('Crags1'))
        self.assertEqual(response.status_code, 302)
        cleanup()
        print("SUCCESS")


    #Method to test if authenticated user receives weather data
    def test_should_return_data_for_logged_in_user(self):
        print("\nTesting that authenticated user receives weather data")
       
        create_user()
        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        response = self.client.get(reverse('Crags1'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Crags1.html')
        cleanup()
        print("SUCCESS")



#Test case for Crag2 
class Crags2Test(TestCase):


    #Method to test if anonymous user is redirected to signin page when requesting crag2
    def test_should_redirect_anonymous_user_to_signin_page(self):
        # self.client.login(username="user", password="password")
        print("\nTesting that anonymous user is redirected to signin page when requesting crag2")
        response = self.client.get(reverse('Crags2'))
        self.assertEqual(response.status_code, 302)
        print("Success")


    #Method to test if authenticated user can access crag2 page
    def test_should_give_access_to_logged_in_user(self):
        print("\nTesting that authenticated user can access crag2 page")

        create_user()
        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        
        response = self.client.get(reverse('Crags2'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Crags2.html')
        cleanup()
        print("SUCCESS")


    #Method to test if authenticated users redirected to Crags3.html view when requesting Crags2 with valid parameters
    def test_should_redirect_user_Crags_view_when_requesting(self):
        print("\nTesting that authenticated users redirected to Crags3.html view when requesting Crags2 with valid parameters")

        create_user()
        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        
        response = self.client.get(reverse('Crags2') + '?Rating=2&Grade=15&Rope Length=False')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Crags3.html')
        cleanup()
        print("SUCCESS")



#Test case for Crag3 
class Crags3Test(TestCase):


    #Method to test if anonymous user is redirected to signin page when requesting Crags3
    def test_should_redirect_anonymous_user_to_signin_page(self):

        print("\nTesting that anonymous user is redirected to signin page when requesting Crags3")

        response = self.client.get(reverse('Crags3'))
        self.assertEqual(response.status_code, 302)

        print("SUCCESS")



    #Method to test if authenticated user can access crags3 page
    def test_should_give_access_to_crags3_page(self):

        print("\nTesting that authenticated user can access crags3 page")

        create_user()

        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        response = self.client.get(reverse('Crags3'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Crags3.html')

        cleanup()

        print("SUCCESS")



#Crags4 simply returns html page



#Test case for Crag5 
class Crag5Test(TestCase):
    

    #Method to test if anonymous user is redirected to signin page when requesting crag5
    def test_should_redirect_anonymous_user_to_signin_page(self):
        # self.client.login(username="user", password="password")
        print("\nTesting that anonymous user is redirected to signin page when requesting crag5")
        response = self.client.get(reverse('Crags5'))
        self.assertEqual(response.status_code, 302)
        print("SUCCESS")


    #Method to test if authenticated user can access crag5 page
    def test_should_give_access_to_logged_in_user(self):
        print("\nTesting that authenticated user can access crag5 page")

        create_user()
        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        
        response = self.client.get(reverse('Crags5'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Crags5.html')
        cleanup()
        print("SUCCESS")

    #Method to ensure that when parameters not equal to 2 (grade and rating), it does not update user level
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


    #Method to ensure that when parameters equal to 2 (grade and rating), it update user level
    def test_should_update_user_level(self):
        print("\nTesting that when parameters equal to 2 (grade and rating), it should update user level")

        create_user()
        self.client.login(username=dummyTestUsername, password=dummyTestPassword)
        user = User.objects.get_by_natural_key(dummyTestUsername)

        prevProfile = userProfile.objects.get(userID=user)
        prevLevel = prevProfile.level
        print("prevLevel: ", prevLevel)

        response = self.client.get(reverse('Crags5') + '?Rating=2&Grade=15')


        currentProfile = userProfile.objects.get(userID=user)
        currentLevel = currentProfile.level
        print("currentLevel: ", currentLevel)

        self.assertEqual(int(log(2*15)) + prevLevel, int(currentLevel))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/MyClimbs')
        cleanup()
        print("SUCCESS")

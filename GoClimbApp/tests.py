from django.test import Client, TestCase
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

testClient = Client()
class t1_AuthenticationTests(TestCase):
    userDetails  = {
        'username':'testUser',
        'email':'testUser@test.com',
        'password1':'password',
        'password2':'password'
    }  
    def test1_SignUp(self):  
        print("Testing SignUp:\n")
        response = testClient.post('/signUp', self.userDetails)
        print("SignUp status code: ", response.status_code)
        self.assertEquals(response.status_code, 200)
    def test2_SignIn(self):  
        print("Testing SignIn:\n")
        response = testClient.post('/signIn',{ 'username':self.userDetails['username'], 'password':self.userDetails['password1']})
        print("SignIn status code: ", response.status_code)
        self.assertEquals(response.status_code, 200)
   
class t2_URLTests(TestCase):
    testURLs = ['','index', 'home','Crags','MyClimbs','MyCommunity','Settings']
    def test1_URLs(self):
        for x in self.testURLs:
            print('\n\ntesting URL:/'+ x)
            response = testClient.get("/"+x)
            self.assertIn(response.status_code, [200,302])
            print('SUCCESS')
        
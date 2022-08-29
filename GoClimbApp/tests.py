from django.test import TestCase
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your tests here.

class t1_AuthenticationTests(TestCase):
    userDetails  = {
        'username':'testUser',
        'email':'testUser@test.com',
        'password1':'password',
        'password2':'password'
    }  
    def test1_SignUp(self):  
        print("Testing SignUp:\n")
        response = self.client.post('/signUp', self.userDetails)
        print("SignUp status code: ", response.status_code)
        self.assertEquals(response.status_code, 200)

    def test2_SignIn(self):  
        print("Testing SignIn:\n")
        response = self.client.post('/signIn',{ 'username':self.userDetails['username'], 'password':self.userDetails['password1']})
        print("SignIn status code: ", response.status_code)
        self.assertEquals(response.status_code, 200)
    
class t2_URLTests(TestCase):
    testURLs1 = ['','index','signIn','signUp']
    testURLs2 = ['home','Crags','MyClimbs','MyCommunity','Settings']
    def test1_CommonURLs(self):
        for x in self.testURLs1:
            print('\n\ntesting Common URL:/', x, sep=" ")
            response = self.client.get("/"+x)
            self.assertEquals(response.status_code, 200)
            print('SUCCESS')
        
    def test2_UserSpecificURLs(self):
        return 0 

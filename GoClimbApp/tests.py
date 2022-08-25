from urllib import response
from django.test import TestCase

# Create your tests here.
class URLTests(TestCase):
    testURLs = ['','index','home','signIn','signUp','Crags','MyClimbs','MyCommunity','Settings']
    def test(self):
        for x in self.testURLs:
            response = self.client.get("/"+x)
            print('testing URL:/', x, sep=" ")
            self.assertEquals(response.status_code, 200)
            print('SUCCESS')      


from django.test import TestCase
from django.contrib.auth.models import User
from user.models import Profile

class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.user = User.objects.create_user(username='test', password='Agniva@2004')

    def test_str_method(self):
        
        profile = self.user.profile
        expected_str = f'{self.user.username}-Profile'
        self.assertEqual(str(profile), expected_str)

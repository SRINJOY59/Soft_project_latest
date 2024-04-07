# from django.test import TestCase
# from django.contrib.auth.models import User
# from user.models import Profile

# class ProfileModelTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username='chiradeep', password='123@Srinjoy')

        
#     def test_profile_creation(self):
#         profile = Profile.objects.create(staff=self.user, address='Test Address', phone='1234567890')
#         self.assertEqual(profile.staff, self.user)
#         self.assertEqual(profile.address, 'Test Address')
#         self.assertEqual(profile.phone, '1234567890')
#         self.assertEqual(profile.image.url, 'Profile_Images/default.png')  # Check default image URL

#     def test_profile_str_representation(self):
#         profile = Profile.objects.create(staff=self.user, address='Test Address', phone='1234567890')
#         self.assertEqual(str(profile), 'testuser-Profile')

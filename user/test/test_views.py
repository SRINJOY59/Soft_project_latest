from django.test import TestCase, Client
from django.urls import reverse
from user.models import Profile
import json

class TestViews(TestCase):
    def test_project_list_GET(self):
        client = Client()
        response = client.get('profile')
        print(response)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')
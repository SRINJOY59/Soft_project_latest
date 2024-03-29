from django.test import TestCase, Client
from django.urls import reverse
from user.models import Profile
import json

class TestViews(TestCase):
    def test_project_list_GET(self):
        client = Client()
        url = reverse('dashboard-index') 
        response = client.get(url)

        self.assertEquals(response.status_code, 302)  

        self.assertTemplateUsed(response, 'dashboard/index.html')

        self.assertContains(response, '<html>')  

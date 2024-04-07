from django.test import SimpleTestCase
from django.urls import reverse, resolve
from staff.views import activate

class TestUrls(SimpleTestCase):
    
    def test_activate_url_is_resolved(self):
        url=reverse('staff-activate', args=[1])
        print(resolve(url))
        self.assertEqual(resolve(url).func, activate)
        
        
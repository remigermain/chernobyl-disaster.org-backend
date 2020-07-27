from django.urls import reverse
from django.contrib.auth.models import User
import requests


def send_mail():
    data = {
        'username': 'username',
        'email': 'email@email.email',
        'password1': 'ApasswordAb123',
        'password2': 'ApasswordAb123',
    }
    # check response
    User.objects.filter(username=data['username']).delete()
    return requests.post('http://localhost:8000' + reverse('api:rest_register'), data)

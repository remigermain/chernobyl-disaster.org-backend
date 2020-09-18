#!/usr/bin/python3
import requests


def send_mail():
    print("send email\n")
    data = {
        'username': 'username',
        'email': 'gifjan@tmpemails.com',
        'password1': 'ApasswordAb123',
        'password2': 'ApasswordAb123',
    }
    # check response
    # get_user_model().objects.filter(username=data['username']).delete()
    resp = requests.post('http://localhost:8000/auth/registration/', data)
    print("email sended\n")
    print(resp.status_code)
    print(resp.content)


requests.get('http://localhost:8000/auth/supp/')
send_mail()

from django.shortcuts import render
import vk, requests


def index(request):
    if not request.COOKIES:
        return render(request, 'index/index.html')
    else:

        return login(request, request.COOKIES['default'])


def authorization(request):
    r = requests.Request('GET',
                         "https://oauth.vk.com/access_token?client_id=6750428&client_secret=99v18EIjTUbof4DmsXVg&redirect_uri=http://139.59.142.85:8000/authorization&code=" +
                         request.GET['code']).prepare()
    response = requests.session().send(r)
    json = response.json()
    return login(request, json['access_token'])


def login(request, access_token):
    session = vk.Session(access_token=access_token)
    api = vk.API(session)
    loggedUser = api.users.get(v=5.87)
    data = dict()
    data['items'] = []
    data['loggedUser'] = loggedUser[0]['first_name'] + ' ' + loggedUser[0]['last_name']
    usrFriends = api.friends.get(order='random', v=5.87, count=5)
    for i in usrFriends['items']:
        cur = api.users.get(user_ids=i, v=5.87)
        data['items'].append(cur[0]['first_name'] + ' ' + cur[0]['last_name'])

    rvalue = render(request, 'index/container.html', data)
    rvalue.set_cookie('default', access_token, expires=600)
    return rvalue

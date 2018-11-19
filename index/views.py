from django.shortcuts import render
import vk, requests


dataBase = dict()
appId = 6750428 #my appId

def createOauthRequest():
    ref = 'https://oauth.vk.com/authorize'
    redirect_uri = "redirect_uri=../login&"
    display = 'display=popup&'
    scope = 'scope=friends&'
    response_type = 'response_type=code&'
    v = 'v=5.87'
    return ref + '?client_id=' + str(appId) + '$' + display + redirect_uri + scope + response_type + v

def index(request):
    return render(request, 'index/index.html')

def authorization(request):
    return login(request)

def login(request, reentry = False):
    try:
        if reentry:
            splitlist = list(dataBase[request.COOKIES['csrftoken']].split())
            usrName = (splitlist[0])
            usrPass = (splitlist[1])
        else:
            usrName = (request.POST['username'])
            usrPass = (request.POST['password'])

        session = vk.AuthSession(appId, usrName, usrPass)
        if not reentry:
            dataBase[request.COOKIES['csrftoken']] = usrName + ' ' + usrPass

        api = vk.API(session)

        loggedUser = api.users.get(v = 5.87)
        data = dict()
        data['items'] = []
        data['loggedUser'] = loggedUser[0]['first_name'] + ' ' + loggedUser[0]['last_name']

        usrFriends = api.friends.get(order='random', v=5.87)
        counter = 0

        for i in usrFriends['items']:
            cur = api.users.get(user_ids = i, v = 5.87)
            data['items'].append(cur[0]['first_name'] + ' ' + cur[0]['last_name'])
            counter += 1
            if counter >= 5:
                break

        return render(request, 'index/container.html', data)

    except:
        #return authorization(request, True)
        pass


import requests
import json
import os
import time


headers = {
        'authorization': 'Bearer 8icaSqRBrp3DTsn2IonoWW4BFxCyDm9rwTVXUiVO',
        'cache-control': 'no-cache',
    }

## Individual User's Chat Extraction Starts from Here
def create_list_of_users():
    users = {}
    url = "https://api.hipchat.com/v2/user?max-results=1000"
    users_headers = {
        'authorization': "Bearer 8icaSqRBrp3DTsn2IonoWW4BFxCyDm9rwTVXUiVO",
        'cache-control': "no-cache",
        'postman-token': "26784681-6ef9-d4bd-826f-977015edc0a2"
        }
    response = requests.request("GET", url, headers=headers)
    check_and_wait(response.headers)
    user_list_dict = response.json()
    items = user_list_dict[u'items']
    for entry in items:
        users[entry[u'mention_name']] = entry[u'id']

    with open('users.json', 'w') as user_file:
        user_file.write(json.dumps(users))

    return users

def get_chat_for_indivdual_user(users_dict):
    dirName = 'oneOoneMessages'
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:
        print("Directory " , dirName ,  " already exists")

    chat_headers = {
        'authorization': "Bearer 8icaSqRBrp3DTsn2IonoWW4BFxCyDm9rwTVXUiVO",
        'cache-control': "no-cache",
        'postman-token': "7263f86d-6283-e466-263b-3cf6992a68ee"
        }

    for key, value in users_dict.iteritems():
        filename = 'oneOoneMessages/{}.json'.format(get_user_name(value))
        url = "https://api.hipchat.com/v2/user/{}/history?max-results=1000".format(value)
        response = requests.request("GET", url, headers=headers)
        check_and_wait(response.headers)
        user_messages = response.json()

        if len(user_messages["items"]) == 0:
            continue

        with open(filename, 'w') as messages_file:
            messages_file.write(response.text)


def get_user_name(id):
    url = "https://api.hipchat.com/v2/user/{}".format(id)

    response = requests.request("GET", url, headers=headers)
    check_and_wait(response.headers)
    user_details = response.json()
    name = user_details[u'mention_name']
    return name

def check_and_wait(headers):
    print('Remaining Hits:{}'.format(headers['X-Ratelimit-Remaining']))
    if int(headers['X-Ratelimit-Remaining']) < 10:
        print('Api Hit Limit is Exceeding...')
        print('Going to Sleep BRB in 1 Mins...')
        time.sleep(60)
        print('Came Back...')


## Individual User's Chat Extraction End's Here

## Room Chat Extraction Starts from Here

def get_rooms_list():

    rooms = {}
    url = "https://api.hipchat.com/v2/room"
    querystring = {"max-results":"1000","include-private":"true","include-archived":"true"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    check_and_wait(response.headers)
    room_list_dict = response.json()
    items = room_list_dict[u'items']
    for entry in items:
        rooms[entry[u'name']] = entry[u'id']

    with open('rooms.json', 'w') as rooms_file:
        rooms_file.write(json.dumps(rooms))

    return rooms

def get_chat_for_indivdual_room(rooms_dict):
    dirName = 'roomMessages'
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created ")
    else:
        print("Directory " , dirName ,  " already exists")

    chat_headers = {
        'authorization': "Bearer 8icaSqRBrp3DTsn2IonoWW4BFxCyDm9rwTVXUiVO",
        'cache-control': "no-cache",
        'postman-token': "7263f86d-6283-e466-263b-3cf6992a68ee"
        }

    for key, value in rooms_dict.iteritems():
        filename = '{}/{}.json'.format(dirName, get_room_name(value))
        url = "https://api.hipchat.com/v2/room/{}/history?max-results=1000".format(value)
        response = requests.request("GET", url, headers=headers)
        check_and_wait(response.headers)
        user_messages = response.json()

        if len(user_messages["items"]) == 0:
            continue

        with open(filename, 'w') as messages_file:
            messages_file.write(response.text)

def get_room_name(id):
    url = "https://api.hipchat.com/v2/room/{}".format(id)

    response = requests.request("GET", url, headers=headers)
    check_and_wait(response.headers)
    room_details = response.json()
    name = room_details[u'name']
    name = name.replace(" ","")
    return name


## Room Chat Extraction Starts from Here

if __name__ == "__main__":
    users_dict = create_list_of_users()
    get_chat_for_indivdual_user(users_dict)
    rooms = get_rooms_list()
    get_chat_for_indivdual_room(rooms)

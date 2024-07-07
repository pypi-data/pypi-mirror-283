import requests

def getmessage():
    return requests.get('http://paketapi.pythonanywhere.com/daymessage').text

def getbootcode():
    return requests.get('http://paketapi.pythonanywhere.com/bootcode').text
    
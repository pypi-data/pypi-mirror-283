import requests

def check_internet_connection():
    try:
        response=requests.get("https://google.com")
        return True
    except:
        return False
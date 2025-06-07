import requests

session = requests.Session()
response = session.get('http://google.com')
print(session.cookies.get_dict())
from requests import get, post, delete, put
from models.person import Person
import datetime

print(get('http://localhost:5000/persons/4').json())
print(put('http://localhost:5000/persons/4', json={'inn': 15135789,
                                                   'type': 'physic',
                                                   'shifer': 6676,
                                                   'veriety': 1,
                                                   'status': 1,
                                                   'email': 'clone12@mail.ru',
                                                   'phone': '89298213318'}).json())
print(post('http://localhost:5000/persons', json={'inn': 15135789,
                                                   'type': 'physic',
                                                   'shifer': 6676,
                                                   'veriety': 1,
                                                   'status': 1,
                                                   'email': 'clone12@mail.ru',
                                                   'phone': '89298213318'}).json())

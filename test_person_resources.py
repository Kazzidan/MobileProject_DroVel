from requests import get, post, delete
from models.person import Person
import datetime

print(get('http://localhost:5000/persons').json())
print(post('http://localhost:5000/persons', json={'inn': 15935789,
                                                  'type': 'physic',
                                                  'shifer': 9999,
                                                  'veriety': 1,
                                                  'status': 1,
                                                  'email': 'clown213124@mail.ru',
                                                  'phone': '8929821338'
                                                  }).json())

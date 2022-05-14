from requests import get, post, delete
from models.person import Person
import datetime

print(get('http://localhost:5000/persons/4').json())

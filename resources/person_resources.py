import datetime

from flask import jsonify
from flask_restful import Resource, abort

from models import db_session
from models.person import Person
from models.phonePerson import PhonePerson
from models.emailPerson import EmailPerson
from resources.reqparse_person import parser


def abort_if_person_not_found(person_id):
    session = db_session.create_session()
    users = session.query(Person).get(person_id)
    if not users:
        abort(404, message=f"Person {person_id} not found")


class PersonsResource(Resource):
    def get(self, person_id):
        abort_if_person_not_found(person_id)
        session = db_session.create_session()
        persons = session.query(Person).get(person_id)
        return jsonify({'person': persons.to_dict(only=('inn', 'type', 'shifer', 'date',
                                                        'veriety', 'status'))})

    def delete(self, person_id):
        abort_if_person_not_found(person_id)
        session = db_session.create_session()
        person = session.query(Person).get(person_id)
        session.delete(person)
        session.commit()
        return jsonify({'success': 'OK'})


class PersonsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        person = session.query(Person).all()
        return jsonify({'persons': [item.to_dict(only=('inn', 'type', 'shifer', 'date',
                                                       'veriety', 'status')) for item in person]})

    def post(self):
        data = parser.parse_args()
        if Person.find_by_inn(data['inn']):
            return jsonify(
                message='Inn is already registered')
        if Person.find_by_shifer(data['shifer']):
            return jsonify(
                message='Shifer is already registered')
        else:
            new_person = Person(
                inn=data['inn'],
                type=data['type'],
                shifer=data['shifer'],
                veriety=data['veriety'],
                status=data['status']
            )
            new_phone = PhonePerson(
                personId=new_person.get_id(),
                phone=data['phone']
            )
            new_email = EmailPerson(
                personId=new_person.get_id(),
                email=data['email']
            )
            try:
                new_person.save_to_db()
                new_phone.save_to_db()
                new_email.save_to_db()
                return jsonify(
                    message='Person {} was created'.format(data['inn'])
                )
            except:
                return jsonify(
                    message='Something went wrong')

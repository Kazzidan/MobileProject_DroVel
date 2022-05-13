import datetime

from flask import jsonify
from flask_restful import Resource, abort

from models import db_session
from models.person import Person
from models.phonePerson import PhonePerson
from models.emailPerson import EmailPerson
from resources.reqparse_person import parser
from resources.reqparse_email import parser_email
from resources.reqparse_phone import parser_ph


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
                                                       'veriety', 'status'))
                                    for item in person]})

    def post(self):
        data_per = parser.parse_args()
        data_ph = parser_ph.parse_args()
        data_email = parser_email.parse_args()
        if Person.find_by_inn(data_per['inn']):
            return jsonify(
                message='Inn is already registered')
        if Person.find_by_shifer(data_per['shifer']):
            return jsonify(
                message='Shifer is already registered')
        else:
            session = db_session.create_session()
            person = session.query(Person).all()
            new_person = Person(
                inn=data_per['inn'],
                type=data_per['type'],
                shifer=data_per['shifer'],
                veriety=data_per['veriety'],
                status=data_per['status']
            )
            length = len([item.to_dict(only=('inn', 'type', 'shifer', 'date',
                                             'veriety', 'status'))
                          for item in person])
            print(length)
            new_phone = PhonePerson(
                personId=length + 1,
                phone=data_ph['phone']
            )
            new_email = EmailPerson(
                personId=length + 1,
                email=data_email['email']
            )
            try:
                new_person.save_to_db()
                new_phone.save_to_db()
                new_email.save_to_db()
                return jsonify(
                    message='Person {} was created'.format(data_per['inn'])
                )
            except:
                return jsonify(
                    message='Something went wrong')

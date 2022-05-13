from flask import jsonify
from flask_restful import Resource, abort

from models import db_session
from models.emailPerson import EmailPerson
from resources.reqparse_person import parser


def abort_if_person_not_found(email_id):
    session = db_session.create_session()
    emails = session.query(EmailPerson).get(email_id)
    if not emails:
        abort(404, message=f"Email {email_id} not found")


class EmailsResource(Resource):
    def get(self, email_id):
        abort_if_person_not_found(email_id)
        session = db_session.create_session()
        emails = session.query(EmailPerson).get(email_id)
        return jsonify({'email': emails.to_dict(only=('personId', 'email'))})

    def delete(self, email_id):
        abort_if_person_not_found(email_id)
        session = db_session.create_session()
        email = session.query(EmailPerson).get(email_id)
        session.delete(email)
        session.commit()
        return jsonify({'success': 'OK'})


class EmailsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        email = session.query(EmailPerson).all()
        return jsonify({'emails': [item.to_dict(only=('personId', 'email')) for item in email]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        email = EmailPerson(
            personId=args['personId'],
            email=args['email']
        )
        session.add(email)
        session.commit()
        return jsonify({'success': 'OK'})

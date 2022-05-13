import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class PhonePerson(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'phone'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    personId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("persons.id"))
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    person = orm.relation("Person")

    def __repr__(self):
        return f'<PhonePerson> {self.id} {self.personId} {self.phone}'

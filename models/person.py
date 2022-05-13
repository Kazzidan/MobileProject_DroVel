import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from models import db_session
from .db_session import SqlAlchemyBase

association_table_veriety = sqlalchemy.Table('associationVeriety', SqlAlchemyBase.metadata,
                                             sqlalchemy.Column('persons', sqlalchemy.Integer,
                                                               sqlalchemy.ForeignKey('persons.id')),
                                             sqlalchemy.Column('veriety', sqlalchemy.Integer,
                                                               sqlalchemy.ForeignKey('veriety.id'))
                                             )

association_table_status = sqlalchemy.Table('associationStatus', SqlAlchemyBase.metadata,
                                            sqlalchemy.Column('persons', sqlalchemy.Integer,
                                                              sqlalchemy.ForeignKey('persons.id')),
                                            sqlalchemy.Column('status', sqlalchemy.Integer,
                                                              sqlalchemy.ForeignKey('status.id'))
                                            )


class Veriety(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'veriety'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    veriety = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class Status(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'status'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class Person(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'persons'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    inn = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    shifer = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    veriety = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("veriety.id"))
    status = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("status.id"))

    phone = orm.relation("PhonePerson", back_populates='person')
    email = orm.relation("EmailPerson", back_populates='person')

    verieties = orm.relation("Veriety",
                             secondary="associationVeriety",
                             backref="persons")
    statuses = orm.relation("Status",
                            secondary="associationStatus",
                            backref="persons")

    def __repr__(self):
        return f'<Colonist> {self.id} {self.Inn}'

    def save_to_db(self):
        session = db_session.create_session()
        session.add(self)
        session.commit()

    def get_id(self):
        return self.id

    @classmethod
    def find_by_inn(cls, inn):
        session = db_session.create_session()
        return session.query(Person).filter(Person.inn == inn).first()
        # return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_shifer(cls, shifer):
        session = db_session.create_session()
        return session.query(Person).filter(Person.shifer == shifer).first()
        # return cls.query.filter_by(email=email).first()

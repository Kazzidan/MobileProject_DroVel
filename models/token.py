import datetime

import redis
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from models import db_session
from .db_session import SqlAlchemyBase


# jwt_redis_blocklist = redis.StrictRedis(
#     host="localhost", port=5000, db=0, decode_responses=True
# )


class RevokedTokenModel(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'revoked_tokens'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    jti = sqlalchemy.Column(sqlalchemy.String(120), nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

    @staticmethod
    def is_jti_blacklisted(jti):
        session = db_session.create_session()
        query = session.query(RevokedTokenModel).filter(RevokedTokenModel.jti == jti).scalar()
        return query

    def save_to_db(self):
        session = db_session.create_session()
        session.add(self)
        session.commit()

import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    nickname = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    speciality = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    jobs = orm.relation("Jobs", back_populates='user')
    services = orm.relation("Services", back_populates='user')

    def __repr__(self):
        return f'<User> [{self.id}] {self.nickname}: {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

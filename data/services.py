import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = 'services'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    service = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    contractor = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    price = sqlalchemy.Column(sqlalchemy.Float)
    preview = sqlalchemy.Column(sqlalchemy.LargeBinary)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    action = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    user = orm.relation('user')

    def __repr__(self):
        return f'<Services> [{self.id}] {self.service}: {self.contractor}, {self.action}'

import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    client = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float)
    preview = sqlalchemy.Column(sqlalchemy.LargeBinary)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    action = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    user = orm.relation('User')

    def __repr__(self):
        return f'<Job> [{self.id}] {self.job}: {self.client}, {self.action}'

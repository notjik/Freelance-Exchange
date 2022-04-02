import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Branch(SqlAlchemyBase):
    __tablename__ = 'branches'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    specialization = sqlalchemy.Column(sqlalchemy.String)
    branches = orm.relation("Services", back_populates='branch')

    def __repr__(self):
        return f'<Branch> [{self.id}]: {self.specialization}'

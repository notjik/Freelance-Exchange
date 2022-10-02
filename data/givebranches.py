from data import db_session
from data.branches import Branch

db_session.global_init("db/freelance_exchange.db")


def bran():
    db_sess = db_session.create_session()
    branches = db_sess.query(Branch).all()
    return [('', 'Выберите категорию')] + [(branch.id, branch.specialization) for branch in branches]

from ..models import db
from ..utils.security import user_datastore
from flask_security import hash_password


def create_dev_db():
    db.create_all()
    if not user_datastore.find_user(email="narendra@gmail.com"):
        user_datastore.create_user(
            username="narendra", email="narendra@gmail.com",
            password=hash_password("1234"))
        db.session.commit()


def create_prod_db():
    db.create_all()

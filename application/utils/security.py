from flask_security import Security, SQLAlchemyUserDatastore
from ..models import db
from ..models.users import Role, User

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
sec = Security()

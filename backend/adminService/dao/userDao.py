
from sqlalchemy.orm import sessionmaker

from database.dbConfig import DatabaseEngine
from database.schemas.userSchema import UserSchema


class UserDao:
    def __init__(self):
        self.engine = DatabaseEngine.getInstance().getEngine()
    
    def getUsers(self):
        session = sessionmaker(bind=self.engine)()
        users = session.query(UserSchema).all()
        session.close()
        return users

    def getUserByEmail(self, email):
        session = sessionmaker(bind=self.engine)()
        user = session.query(UserSchema).filter(UserSchema.email == email).first()
        session.close()
        return user
    
    def updateUserPrivilegeByEmail(self, email, privilege):
        session = sessionmaker(bind=self.engine, autoflush=True)()
        user = session.query(UserSchema).filter(UserSchema.email == email).first()
        user.privilege = privilege
        session.commit()
        session.close()
        return user

    def deleteUserByEmail(self, email):
        session = sessionmaker(bind=self.engine, autoflush=True)()
        try:
            user = session.query(UserSchema).filter(UserSchema.email == email).first()
            session.delete(user)
            session.commit()
            session.close()
        except Exception as e:
            print(e)
            session.rollback()
            session.close()
            return False
        return True

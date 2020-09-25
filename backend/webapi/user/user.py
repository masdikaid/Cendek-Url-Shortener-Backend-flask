from datetime import datetime
from firebase import userRegisterAuth, checkToken, userUpdateData, userDisable, userGet, userGetWithEmail, userGetAll, userRequestVerifyMail, userDelete, userIsVerified, userIsActive


class User():
    def __init__(self, email, uid=None, firstname=None, lastname=None, avatar=None, isadmin=False):
        self.uid = uid
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.avatar = avatar
        self.isadmin = isadmin

    
    def create(self, password):
        user = userRegisterAuth(self.email, password, self.toDict)
        self.uid = user.id
        return self
        
    def update(self):
        userUpdateData(self.uid, self.toDict)
        return self

    def delete(self):
        return userDisable(self.uid)

    def deletePermanent(self):
        return userDelete(self.uid)

    @property
    def toDict(self):
        return {
            "email" : self.email,
            "firstname" : self.firstname,
            "lastname" : self.lastname,
            "avatar" : self.avatar,
            "isadmin" : self.isadmin
        }

    @property
    def isverified(self):
        return userIsVerified(self.uid)

    @property
    def isactive(self):
        return userIsActive(self.uid)

    @staticmethod
    def get(uid):
        user = userGet(uid)
        return User(user["email"], user["uid"], user["firstname"], user["lastname"], user["avatar"], user["isadmin"])

    @staticmethod
    def getWithEmail(email):
        user = userGetWithEmail(email)
        return User(user["email"], user["uid"], user["firstname"], user["lastname"], user["avatar"], user["isadmin"])

    @staticmethod
    def all():
        users = []
        for user in userGetAll() :
            users.append(User(user["email"], user["uid"], user["firstname"], user["lastname"], user["avatar"], user["isadmin"]))
        return users
        
    @staticmethod
    def verifyToken(token):
        return User.get(checkToken(token))

    def sendEmailVerification(self):
        userRequestVerifyMail(self.uid)
        return self

    def __str__(self):
        if self.firstname and self.lastname :
            return self.firstname + " " + self.lastname
        else :
            return self.email

    def __repr__(self):
        return self.__str__()









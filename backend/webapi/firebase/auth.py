import sys
from datetime import datetime
from .setup import auth, db, exceptions, firestore

def userRegisterAuth(email, password, userdata):
    try :
        user = auth.create_user(
                    email = email,
                    password = password,
                )
        userdata["joinat"] = datetime.now()
        userdata = db.collection(u"users").document(user.uid).set(userdata)
        userdata = db.collection(u"users").document(user.uid).get()
        return userdata
    except (ValueError, auth.EmailAlreadyExistsError) as error :
        raise ValueError(error)

def userUpdateData(id, userdata):
    user = db.collection(u"users").document(id)
    user.update(userdata)
    user.update({u"updateat": firestore.ArrayUnion([{str(datetime.now()):userdata}])})

def userDisable(uid):
    auth.update_user(uid, disabled=True)
    return None

def userDelete(uid):
    auth.delete_user(uid)
    db.collection(u"users").document(uid).delete()
    return None

def userGet(uid):
    user = db.collection(u"users").document(uid).get()
    if user.exists :
        userdata = user.to_dict()
        userdata["uid"] = user.id
        return userdata
    else :
        raise ValueError("User Not Found")

def userIsVerified(uid):
    return auth.get_user(uid).email_verified

def userIsActive(uid):
    return not auth.get_user(uid).disabled

def userGetWithEmail(email):
    users = db.collection(u"users").where(u"email", u"==", email).get()
    if len(users) == 1 :
        userdata = users[0].to_dict()
        userdata["uid"] = users[0].id
        return userdata
    elif len(users) > 1 :
        raise ValueError("User Duplicated")
    else :
        raise ValueError("User Not Found")  

def userGetAll():
    users = []
    for user in db.collection(u"users").stream() :
        userdata = user.to_dict()
        userdata["uid"] = user.id
        users.append(userdata)
    return users

def userRequestVerifyMail(uid):
    syncronizeEmail(uid)
    auth.update_user(uid, email_verified=True)

def checkToken(token):
    try :
        user = auth.verify_id_token(token)
        return user["uid"]
    except auth.InvalidIdTokenError :
        raise ValueError("invalid Token")

def syncronizeEmail(uid):
    authemail = auth.get_user(uid).email
    dataemail = db.collection(u"users").document(uid).get().to_dict()["email"]
    if authemail == dataemail :
        return authemail
    else :
        db.collection(u"users").document(uid).set({u"email":authemail}, merge=True)
        return authemail

        

from secrets import token_urlsafe
from random import choice
from .setup import db, exceptions, firestore

def createShorterUrl(urlid, userid, urldata):
    if not urlid :
        urlid = token_urlsafe(choice(range(5,8)))
        while db.collection(u"shortenurl").document(urlid).get().exists :
            urlid = token_urlsafe(choice(range(5,8)))
    if not db.collection(u"shortenurl").document(urlid).get().exists :
        urldata["userid"] = userid
        urldoc = db.collection(u"shortenurl").document(urlid)
        urldoc.set(urldata)
        urldict = urldoc.get().to_dict()
        urldict["urlid"] = urldoc.id
        return urldict
    else :
        raise ValueError("id already axists")

def updateUrlData(urlid, urldata):
    urldata = db.collection(u"shortenurl").document(urlid)
    if urldata.get().exists :
        urldata.update(urldata)
    else :
        raise ValueError("data not found")

def getUrlData(urlid):
    urldata = db.collection(u"shortenurl").document(urlid).get()
    if urldata.exists :
        return urldata.to_dict()
    else :
        raise ValueError("data not found")

def getUrlDataByUser(userid):
    urldata = db.collection(u"shortenurl").where("userid", "==", userid)
    urldata = urldata.where("isactive","==", True).get()
    if len(urldata) > 0 :
        urls = []
        for u in urldata :
            url = u.to_dict()
            url["urlid"] = u.id
            urls.append(url)
        return urls
    else :
        raise ValueError("data not found")

def getAllUrlData(userid):
    urldata = db.collection(u"shortenurl").where("isactive","==",True).get()
    if len(urldata) > 0 :
        urls = []
        for u in urldata :
            url = u.to_dict()
            url["urlid"] = u.id
            urls.append(url)
        return urls
    else :
        raise ValueError("data not found")

def getVisitor(urlid):
    urldata = db.collection(u"shortenurl").document(urlid).get()
    if urldata.exists :
        urldata = urldata.to_dict()
        if "visitor" in urldata and len(urldata["visitor"]) > 0 :
            return urldata["visitor"]
        else :
            raise ValueError("not has visitor yet")
    else :
        raise ValueError("data not found")

def setVisitorData(urlid, visitordata):
    urldata = db.collection(u"shortenurl").document(urlid)
    if urldata.get().exists :
        urldata = urldata.update({u"visitor" : firestore.ArrayUnion([visitordata])})
    else :
        raise ValueError("data not found")

def deleteUrlData(urlid):
    urldata = db.collection(u"shortenurl").document(urlid)
    if urldata.get().exists :
        newurldata = urldata.get().to_dict()
        newurldata["isactive"]=False
        newurldata = db.collection(u"shortenurl").set(urldata)
        urldata.delete()
    else :
        raise ValueError("data not found")

def checkUrlExists(urlid):
    if db.collection(f"shortenurl.{urlid}").get().exists :
        return True
    else :
        return False

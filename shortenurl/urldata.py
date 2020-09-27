from datetime import datetime
from firebase import createShorterUrl,getAllUrlData, getUrlData, getUrlDataByUser, getVisitor, setVisitorData, setExpirationData, updateUrlData, deleteUrlData, checkUrlExists

class UrlStore():
    def __init__(self, target_url=[], urlid=None, userid=None, isactive=True, expiration=None, create_at=None):
        self.urlid = urlid
        self.userid = userid
        self.target_url = self.setTargetUrl(target_url)
        self.isactive = isactive
        self.expiration = expiration
        self.create_at = create_at 
    
    def setTargetUrl(self, target_url):
        if not len(target_url) == 0 :
            return [{ datetime.now().strftime("%Y%m%d%H%M%S%f") : {"title":url["title"] if "title" in url else None, "url":url["url"], "desc":url["desc"] if "desc" in url else None, "thumb":url["thumb"] if "thumb" in url else None}} for url in target_url ]
        else :
            raise ValueError("target url must have minimum one url")

    def create(self):
        self.create_at = datetime.now()
        url_data = createShorterUrl(self.urlid, self.userid, self.toDict)
        self.urlid = url_data["urlid"]

    def update(self):
        updateUrlData(self.urlid, self.toDict)

    def delete(self):
        deleteUrlData(self.urlid)
        return None

    @staticmethod
    def get(urlid):
        urldata = getUrlData(urlid)
        return UrlStore(urldata["target_url"], urlid, urldata["userid"], urldata["isactive"], urldata["expiration"], urldata["create_at"])

    @staticmethod
    def getByUser(userid):
        urlsdata = getUrlDataByUser(userid)
        return [ UrlStore(u["target_url"], u["urlid"], u["userid"], u["isactive"], u["expiration"], u["create_at"]) for u in urlsdata ]

    @staticmethod
    def all(userid):
        urlsdata = getAllUrlData(userid)
        return [ UrlStore(u["target_url"], u["urlid"], u["userid"], u["isactive"], u["expiration"], u["create_at"]) for u in urlsdata ]    

    @property
    def visitor(self):
        return getVisitor(self.urlid)

    @visitor.setter
    def visitor(self, visitordata):
        visitor = {
            "timestamp" : datetime.now(),
            "ipaddress" : visitordata["ipaddress"],
            "device" : visitordata["device"]
        }
        setVisitorData(self.urlid, visitor)

    @expiration.setter
    def expiration(self, expirationdata):
        expiration = {
            "expiration_at" : expirationdata["expiration_at"],
            "expiration_messege" : expirationdata["messege"] 
        }
        setExpirationData(self.urlid, expiration)
        self.expiration = expiration

    @property
    def toDict(self):
        return {
            "target_url" : self.target_url,
            "isactive" : self.isactive,
            "expiration" : self.expiration,
            "create_at" : self.create_at
        }

    @staticmethod
    def check(urlid):
        return checkUrlExists(urlid)

def linkUrl(urlid):
    return "http://ndk.li/" + urlid
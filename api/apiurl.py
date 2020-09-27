from flask_restful import reqparse, Resource
from user import User
from shortenurl import UrlStore, linkUrl

class ApiAnonGetCreateUrl(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
    
    def get(self):
        self.parser.add_argument("chekurl", required=True)
        args = self.parser.parse_args()
        return {"exsists": UrlStore.check(args["checkurl"])}

    def post(self):
        self.parser.add_argument("urls", required=True)
        self.parser.add_argument("expiration")
        args = self.parser.parse_args()
        try :
            url = UrlStore(args["urls"])
            url.create()
            if "expiration" in args:
                url.expiration = args["expiration"]
            urldata = url.toDict
            urldata["id"] = url.urlid
            urldata["url"] = linkUrl(url.urlid)
            return urldata, 201
        except ValueError as e :
            return {"messege": f"{e}"}, 400

class ApiUserGetCreateUrl(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("AuthToken", location="headers", required=True, help="Token Needed")

    def get(self):
        args = self.parser.parse_args()
        if args["AuthToken"] :
            try :
                urlsdata = []
                urls = User.verifyToken(args["AuthToken"]).getShortenUrls()
                for url in urls :
                    urldata = url.toDict
                    urldata["id"] = url.urlid
                    urldata["url"] = linkUrl(url.urlid)
                    urlsdata.append(urldata)
                return urlsdata
            except ValueError as e :
                return {"messege" : f"{e}"}, 400

    def post(self):
        self.parser.add_argument("urlid", required=True, default=None)
        self.parser.add_argument("urls", required=True)
        self.parser.add_argument("expiration")
        args = self.parser.parse_args()
        if args["AuthToken"] :
            try :
                url = UrlStore(args["url"], args["urlid"], User.verifyToken(args["AuthToken"]).uid)
                url.create()
                if "expiration" in args:
                    url.expiration = args["expiration"]
                urldata = url.toDict
                urldata["id"] = url.urlid
                urldata["url"] = linkUrl(url.urlid)
                return urldata, 201
            except ValueError as e :
                return {"messege": f"{e}"}, 400

            

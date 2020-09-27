from flask_restful import reqparse, Resource
from user import User
from shortenurl import UrlStore, linkUrl

class ApiAnonGetCreateUrl(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
    
    def get(self):
        self.parser.add_argument("checkurl", required=True)
        args = self.parser.parse_args()
        return {"exsists": UrlStore.check(args["checkurl"])}

    def post(self):
        self.parser.add_argument("urls", required=True, type=dict, action="append")
        self.parser.add_argument("expiration", type=dict)
        args = self.parser.parse_args()
        try :
            url = UrlStore(args["urls"])
            if "expiration" in args:
                url.expiration = args["expiration"]
            url.create()
            urldata = url.toDict
            urldata["id"] = url.urlid
            urldata["create_at"] = str(urldata["create_at"])
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
                    urldata["create_at"] = str(urldata["create_at"])
                    urldata["url"] = linkUrl(url.urlid)
                    urlsdata.append(urldata)
                return urlsdata
            except ValueError as e :
                return {"messege" : f"{e}"}, 400

    def post(self):
        self.parser.add_argument("urlid", default=None)
        self.parser.add_argument("urls", required=True, type=dict, action="append")
        self.parser.add_argument("expiration", type=dict)
        args = self.parser.parse_args()
        if args["AuthToken"] :
            try :
                url = UrlStore(args["urls"], args["urlid"], User.verifyToken(args["AuthToken"]).uid)
                if "expiration" in args:
                    url.expiration = args["expiration"]
                url.create()
                urldata = url.toDict
                urldata["id"] = url.urlid
                urldata["create_at"] = str(urldata["create_at"])
                urldata["url"] = linkUrl(url.urlid)
                return urldata, 201
            except ValueError as e :
                return {"messege": f"{e}"}, 400

            

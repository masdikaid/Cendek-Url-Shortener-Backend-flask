from flask_restful import reqparse, Resource
from flask import url_for
from user import User
from shortenurl import UrlStore

class ApiAnonGetCreateUrl(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
    
    def get(self):
        self.parser.add_argument("checkurl", required=True)
        args = self.parser.parse_args()
        return {"exists": UrlStore.check(args["checkurl"])}

    def post(self):
        self.parser.add_argument("urls", required=True, type=dict, action="append")
        self.parser.add_argument("expiration", type=dict)
        args = self.parser.parse_args()
        try :
            url = UrlStore(args["urls"])
            url.create()
            if args["expiration"]:
                url.expiration(args["expiration"])
                url.update()
            urldata = url.toDict
            urldata["id"] = url.urlid
            urldata["create_at"] = str(urldata["create_at"])
            urldata["url"] = url_for("getUrl", urlid=url.urlid, _external=True)
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
                    urldata["url"] = url_for("getUrl", urlid=url.urlid, _external=True)
                    urldata["hit"] = url.hit
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
                url.create()
                if args["expiration"]:
                    url.setExpiration(args["expiration"])
                    url.update()
                urldata = url.toDict
                urldata["id"] = url.urlid
                urldata["create_at"] = str(urldata["create_at"])
                urldata["url"] = url_for("getUrl", urlid=url.urlid, _external=True)
                return urldata, 201
            except ValueError as e :
                return {"messege": f"{e}"}, 400

class ApiUserUrlManager(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("AuthToken", location="headers", required=True, help="Token Needed")

    def get(self, urlid):
        args = self.parser.parse_args()
        if args["AuthToken"] :
            try :
                user = User.verifyToken(args["AuthToken"]).uid
                url = UrlStore.get(urlid)
                if url.userid == user :
                    urldata = url.toDict
                    urldata["id"] = url.urlid
                    urldata["create_at"] = str(urldata["create_at"])
                    urldata["url"] = url_for("getUrl", urlid=url.urlid, _external=True)
                    return urldata
                else :
                    return {"messege": "Invalid Auth"}, 400
            except ValueError as e :
                return {"messege": f"{e}"}, 400

    def put(self, urlid):
        self.parser.add_argument("urls", required=True, type=dict, action="append")
        self.parser.add_argument("expiration", type=dict)
        args = self.parser.parse_args()
        if args["AuthToken"] :
            try :
                user = User.verifyToken(args["AuthToken"]).uid
                url = UrlStore.get(urlid)
                if url.userid == user :
                    if args["expiration"] :
                        url.setExpiration(args["expiration"])
                    url.setTargetUrl(args["urls"])
                    url.update()
                    urldata = url.toDict
                    urldata["id"] = url.urlid
                    urldata["create_at"] = str(urldata["create_at"])
                    urldata["url"] = url_for("getUrl", urlid=url.urlid, _external=True)
                    return urldata
                else :
                    return {"messege": "Invalid Auth"}, 400
            except ValueError as e :
                return {"messege": f"{e}"}, 400

    def delete(self, urlid):
        try :
            args = self.parser.parse_args()
            user = User.verifyToken(args["AuthToken"]).uid
            url = UrlStore.get(urlid)
            if url.userid == user :
                url.delete()
                return {"messege": "success"}
            else :
                return {"messege": "Invalid Auth"}, 400
        except ValueError as e :
            return {"messege": f"{e}"}, 400

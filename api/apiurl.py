from flask_restful import reqparse, Resource
from user import User
from shortenurl import UrlStore

class ApiAnonCreateUrl(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument("urls", required=True)
        self.parser.add_argument("expiration")
        args = self.parser.parse_args()
        try :
            url = UrlStore(args["urls"])
            url.create()
            if "expiration" in args:
                url.expiration = args["expiration"]
            return url.toDict
        except ValueError as e :
            return {"messege": f"{e}"}, 400
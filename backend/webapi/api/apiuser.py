from flask_restful import reqparse, Resource
from user import User

class ApiUserRegister(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("firstname", default=None)
        self.parser.add_argument("lastname", default=None)
        self.parser.add_argument("email", required=True, help="Email is Required")
        self.parser.add_argument("password", required=True, help="Password is Required")

    def post(self):
        try :
            args = self.parser.parse_args()
            newuser = User(email=args["email"], firstname=args["firstname"], lastname=args["lastname"])
            newuser.create(args["password"])
            return {"message":"Success"}
        except ValueError as error:
            return {"messege": f"ValueError: {error}"}, 400


class ApiUserManager(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("AuthToken", location="headers", required=True, help="Token Needed")

    def get(self, user_id):
        args = self.parser.parse_args()
        if args["AuthToken"] :
            try :
                user = User.verifyToken(args["AuthToken"])
                return user.toDict
            except ValueError as e :
                return {"messege": f"{e}"}, 403
        else :
            return {"messege" : "Token is needed"}, 400
    
    def put(self, user_id):
        self.parser.add_argument("firstname")
        self.parser.add_argument("lastname")
        self.parser.add_argument("avatar")
        args = self.parser.parse_args()
        if args["AuthToken"] :
            try :
                user = User.verifyToken(args["AuthToken"])
                if args["firstname"] :
                    user.firstname = args["firstname"]
                if args["lastname"] :
                    user.lastname = args["lastname"]
                if args["avatar"] :
                    user.avatar = args["avatar"]
                user.update()
                return {"message":"Success"}
            except ValueError as e :
                return {"messege": f"{e}"}, 403
        else :
            return {"messege" : "Token is needed"}, 400



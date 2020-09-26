from flask_restful import reqparse, Resource
from user import User

class ApiAdminGetCreateUser(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("AuthToken", location="headers", required=True, help="Token Needed")

    def get(self):
        args = self.parser.parse_args()
        try :
            if User.verifyToken(args["AuthToken"]).isadmin :
                users = []
                for user in User.all() :
                    datauser = user.toDict
                    datauser["id"] = user.uid
                    users.append(datauser)
                return users
            else :
                return {"messege":"User isn't Admin"}, 403
        except ValueError as e : 
            return {"messege": f"ValueError: {e}"}, 400

    def post(self):
        self.parser.add_argument("firstname", default=None)
        self.parser.add_argument("lastname", default=None)
        self.parser.add_argument("isadmin", default=False, type=bool)
        self.parser.add_argument("email", required=True, help="Email is Required")
        self.parser.add_argument("password", required=True, help="Password is Required")
        args = self.parser.parse_args()
        try :
            if User.verifyToken(args["AuthToken"]).isadmin :
                newuser = User(email=args["email"], firstname=args["firstname"], lastname=args["lastname"], isadmin=args["isadmin"])
                newuser.create(args["password"])
                return {"message":"Success"}
            else :
                return {"messege":"User isn't Admin"}, 403
        except ValueError as error:
            return {"messege": f"ValueError: {error}"}, 400


class ApiAdminUserManager(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("AuthToken", location="headers", required=True, help="Token Needed")

    def get(self, user_id):
        args = self.parser.parse_args()
        try :
            if User.verifyToken(args["AuthToken"]).isadmin :
                user = User.get(user_id)
                datauser = user.toDict
                datauser["id"] = user.uid
                return datauser
            else :
                return {"messege":"User isn't Admin"}, 403
        except ValueError as e : 
            return {"messege": f"ValueError: {e}"}, 400
    
    def put(self, user_id):
        self.parser.add_argument("firstname")
        self.parser.add_argument("lastname")
        self.parser.add_argument("isadmin")
        args = self.parser.parse_args()
        try :
            if User.verifyToken(args["AuthToken"]).isadmin :
                user = User.get(user_id)
                if args["firstname"] :
                    user.firstname = args["firstname"]
                if args["lastname"] :
                    user.lastname = args["lastname"]
                if args["isadmin"] :
                    user.isadmin = args["isadmin"]
                if args["avatar"] :
                    user.avatar = args["avatar"]
                user.update()
                return {"message":"Success"}
            else :
                return {"messege":"User isn't Admin"}, 403
        except ValueError as error :
            return {"messege":f"ValueError : {error}"}, 400

    def delete(self, user_id):
        args = self.parser.parse_args()
        try :
            if User.verifyToken(args["AuthToken"]).isadmin :
                User.get(user_id).delete()
                return {"message":"Success"}
            else :
                return {"messege":"User isn't Admin"}, 403
        except ValueError as error :
            return {"messege":f"ValueError : {error}"}, 400
import sys
sys.path.append("d:\\project\\cendek-url-shorter\\backend\\webapi")
from user import User
from flask import Flask
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)


class apiUserRegister(Resource):
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
            

class apiAdminGetAllUser(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("AuthToken", location="headers", required=True, help="Token Needed")

    def get(self):
        args = self.parser.parse_args()
        try :
            if User.verifyToken(args["AuthToken"])["isadmin"] :
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


class apiAdminUserManager(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("AuthToken", location="headers", required=True, help="Token Needed")

    def get(self, user_id):
        args = self.parser.parse_args()
        try :
            if User.verifyToken(args["AuthToken"])["isadmin"] :
                user = User.get(user_id)
                datauser = user.toDict
                datauser["id"] = user.uid
                return datauser
            else :
                return {"messege":"User isn't Admin"}, 403
        except ValueError as e : 
            return {"messege": f"ValueError: {e}"}, 400

    def post(self):
        self.parser.add_argument("firstname", default=None)
        self.parser.add_argument("lastname", default=None)
        self.parser.add_argument("email", required=True, help="Email is Required")
        self.parser.add_argument("password", required=True, help="Password is Required")
        self.parser.add_argument("isadmin", required=True, help="isadmin state is required")
        args = self.parser.parse_args()
        try :
            if User.verifyToken(args["AuthToken"])["isadmin"] :
                newuser = User(email=args["email"], firstname=args["firstname"], lastname=args["lastname"], isadmin=args["isadmin"])
                newuser.create(args["password"])
                newuser.sendEmailVerification()
                return {"message":"Success"}
            else :
                return {"messege":"User isn't Admin"}, 403
        except ValueError as error:
            return {"messege": f"ValueError: {error}"}, 400
    
    def put(self, user_id):
        self.parser.add_argument("firstname")
        self.parser.add_argument("lastname")
        self.parser.add_argument("isadmin")
        args = self.parser.parse_args()
        try :
            if User.verifyToken(args["AuthToken"])["isadmin"] :
                user = User.get(user_id)
                if args["firstname"] :
                    user.firstname = args["firstname"]
                if args["lastname"] :
                    user.lastname = args["lastname"]
                if args["isadmin"] :
                    user.isadmin = args["isadmin"]
                user.update()
                return {"message":"Success"}
            else :
                return {"messege":"User isn't Admin"}, 403
        except ValueError as error :
            return {"messege":f"ValueError : {error}"}, 400

    def delete(self, user_id):
        args = self.parser.parse_args()
        try :
            if User.verifyToken(args["AuthToken"])["isadmin"] :
                User.get(user_id).delete()
                return {"message":"Success"}
            else :
                return {"messege":"User isn't Admin"}, 403
        except ValueError as error :
            return {"messege":f"ValueError : {error}"}, 400

api.add_resource(apiUserRegister, '/account/signup/')
api.add_resource(apiAdminGetAllUser, '/admin/users/')
api.add_resource(apiAdminUserManager, '/admin/users/<string:user_id>/')

if __name__ == '__main__':
    app.run(debug=True)
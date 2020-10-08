import sys, os
sys.path.append(os.path.dirname(__file__))
from api import ApiUserRegister, ApiUserManager, ApiAdminGetCreateUser, ApiAdminUserManager, VerificationHandler, ApiUserGetCreateUrl, ApiAnonGetCreateUrl, ApiUserUrlManager
from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app)          

api.add_resource(ApiAnonGetCreateUrl, '/')
api.add_resource(ApiUserManager, '/account/')
api.add_resource(ApiUserRegister, '/account/signup/')
api.add_resource(ApiUserGetCreateUrl, '/account/urls/')
api.add_resource(ApiUserUrlManager, '/account/urls/<string:urlid>/')
api.add_resource(VerificationHandler, '/account/verification/')
api.add_resource(ApiAdminGetCreateUser, '/admin/users/')
api.add_resource(ApiAdminUserManager, '/admin/users/<string:user_id>/')

@app.route("/<sring:urlid")

if __name__ == '__main__':
    app.run(debug=True)
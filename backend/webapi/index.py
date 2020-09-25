import sys
sys.path.append("d:\\project\\cendek-url-shorter\\backend\\webapi")
from api import ApiUserRegister, ApiUserManager, ApiAdminGetCreateUser, ApiAdminUserManager
from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app)          


api.add_resource(ApiUserRegister, '/account/signup/')
api.add_resource(ApiUserManager, '/account/<string:user_id>')
api.add_resource(ApiAdminGetCreateUser, '/admin/users/')
api.add_resource(ApiAdminUserManager, '/admin/users/<string:user_id>/')

if __name__ == '__main__':
    app.run(debug=True)
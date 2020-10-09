import sys, os, datetime
sys.path.append(os.path.dirname(__file__))
from api import ApiUserRegister, ApiUserManager, ApiAdminGetCreateUser, ApiAdminUserManager, VerificationHandler, ApiUserGetCreateUrl, ApiAnonGetCreateUrl, ApiUserUrlManager, UrlGetRedirect
from flask import Flask, request, redirect, render_template
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

@app.route("/<string:urlid>")
def getUrl(urlid):
    try :
        url = UrlGetRedirect(urlid).hit(request)    
        if len(url["target_url"]) == 1 :
            return redirect(url["target_url"][0]["url"])
        elif len(url["target_url"]) > 1 :
            return render_template("multi_url_item.html", urldata=url["target_url"])
        else :
            return "<h1>404</h1>"
    except ValueError:
        return "<h1>404</h1>"

if __name__ == '__main__':
    app.run(debug=False)
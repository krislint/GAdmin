from flask import Flask,jsonify,request,redirect


app = Flask(__name__)

from config.config import Config

app.config.from_object(Config)
from DirectoryUtil.create_service import ServiceFactory

from oauth import oauth
app.register_blueprint(oauth,url_prefix="/oauth")

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/user_list")
@app.route("/<name>/user_list")
def test(name="default"):
    res,service = ServiceFactory.getService(name)
    if res:
        data = service.users().list(customer='my_customer', maxResults=5,
                                 orderBy='email').execute()
    else:
        return redirect("/oauth/auth")
    return jsonify(data)


@app.route("/adduser",methods=["post"])
@app.route("/<name>/adduser",methods=["post"])
def adduser(name="default"):
    data_temp = request.get_json()
    data ={
        "name": {
            "familyName": data_temp.get("familyName"),
            "givenName": data_temp.get("givenName")
        },
        "password": data_temp.get("password"),
        "primaryEmail": data_temp.get("account"),
        "changePasswordAtNextLogin": True,
        "orgUnitPath": data_temp.get("orgUnit")
    }
    res, service = ServiceFactory.getService(name)
    info = {"code":500,"msg":"service create failure"}
    if res:
        try:
            info = service.users().insert(body=data).execute()
        except Exception as ex:
            return jsonify(msg=ex.args[1].decode(),code=409)
    return jsonify(info)


@app.route("/orgunit",methods=["get"])
@app.route("/<name>/orgunit",methods=["get"])
def orgunit(name="default"):
    res, service = ServiceFactory.getService(name)
    info = {"code": 500, "msg": "service create failure"}
    if res:
        info = service.orgunits().list(customerId="my_customer").execute()
    return jsonify(info)


@app.route("/loaded_service")
def service_list():
    data = ServiceFactory.get_service_list()
    return jsonify(code=200,msg="success",data=data)

if __name__ == '__main__':
    app.run()

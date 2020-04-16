from google_auth_oauthlib.flow import Flow
from flask import Blueprint,request,redirect

from DirectoryUtil.create_service import ServiceFactory
from utils.fileutil import FileUtil

oauth = Blueprint("oauth",__name__)
from config.config import Config

credentials_path = Config.credentials_file
SCOPES =Config.SCOPES

@oauth.route("/auth")
@oauth.route("/auth/<name>")
def auth(name="default"):
    creds = None
    path = FileUtil.get_file(name)
    creds = FileUtil.obj_load(path)
    if creds and creds.valid:
        return "%s 已授权"%name
    flow = Flow.from_client_secrets_file(
                credentials_path, SCOPES,redirect_uri=Config.HOST_Address+"oauth/token/%s"%name)
    return redirect(flow.authorization_url()[0])

@oauth.route("/token/<name>")
def token(name="default"):
    flow = Flow.from_client_secrets_file(
        credentials_path, SCOPES,redirect_uri=Config.HOST_Address+"oauth/token/%s"%name)
    try:
        resp = request.url.replace("http","https")

        flow.fetch_token(authorization_response=resp)
        creds = flow.credentials
        path = FileUtil.get_file(name)
        FileUtil.write_file(path,creds)
        return "%s 授权成功 请关闭网页"%name
    except Exception as ex:
        print(ex.args)
        return "授权失败"

@oauth.route("/remove/<name>")
def remove_cer(name="default"):
    path = FileUtil.get_file(name)
    FileUtil.delete_file(path)
    ServiceFactory.remove_service(name)

    return "remove service %s success"%name

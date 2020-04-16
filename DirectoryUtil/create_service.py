from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from utils.fileutil import FileUtil

class ServiceFactory:
    cred_map = {}

    @staticmethod
    def get_service_list():
        return ServiceFactory.cred_map.keys()

    @staticmethod
    def remove_service(name:str):
        ServiceFactory.cred_map.pop(name)


        return True
    @classmethod
    def getcreds(cls,name:str):
        creds = cls.cred_map.get(name,None)
        if  creds == None:
            res,creds = getCreds(name)
            if res:
                cls.cred_map[name] = creds
            else:
                return False,None
        return True, creds

    @classmethod
    def getService(cls,name:str):
        res,creds = cls.getcreds(name)
        if not res:
            return False,None

        return True,getService(creds,name)

def getCreds(name:str):
    creds = None
    token_path = FileUtil.get_file(name)
    creds = FileUtil.obj_load(token_path)
    if not creds:
        return False,"凭证异常"

    return True,creds

def getService(creds,name):
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path = FileUtil.get_file(name)
        FileUtil.write_file(token_path,creds)
    service = build('admin', 'directory_v1', credentials=creds)

    return service

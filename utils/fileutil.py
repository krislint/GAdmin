import os.path
import pickle
from flask import current_app
from config.config import Config


class FileUtil(object):

    @staticmethod
    def get_file(file_name = "default")->str:
        return os.path.join(current_app.root_path,Config.token_dir,"%s.pickle"%file_name)

    @staticmethod
    def write_file(path:str,obj:object):
        with open(path, 'wb') as token:
            pickle.dump(obj, token)

    @staticmethod
    def delete_file(path):
        if os.path.exists(path):
            os.remove(path)
        return True


    @staticmethod
    def obj_load(path)->object:
        creds = None
        if os.path.exists(path):
            with open(path, 'rb') as token:
                creds = pickle.load(token)
        return creds
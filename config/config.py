class Config(object):
    Client_ID=""
    Client_Secret=""
    SCOPES = [
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/admin.directory.orgunit'
    ]
    DEFAULT_RETURN_Url = "/"

    HOST_Address = "http://localhost:5000/"
    credentials_file = "config/credentials.json"
    token_dir = "config"
    #GSUITE_DOMAIN = "bmedu.org"
    #orgUnitPath="/PA USERS - ONLINE"

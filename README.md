### 多全局分发GSuite账号

只负责创建不负责其他（包括不验证是否存在，这些交给google的api来），如需权限管理请自己套一层api
这也非常符合微服务的概念。。。。（主要是懒）

### 如何部署

请先到google cloud 弄个oauth2 然后下载credentials.json 放到config目录下
另外复制一下Client_ID 以及Client_Secret到config.py

请确保可以访问Google
pip install -r requirement.txt

python app.py


### 使用说明

添加授权：  /oauth/auth/< name:后续用到的服务名 > 授权 注意服务名唯一

删除授权 /remove/< name >

查看用户组 /< name >/orgunit

以动态加载的服务 /loaded_service

用户列表 /< name >/user_list

新增用户： 

post 方法请求 /< name:之前的服务名 >/adduser

```
    data_temp = request.get_json()
    data ={
        "name": {
            "familyName": data_temp.get("familyName"),
            "givenName": data_temp.get("givenName")
        },
        "password": data_temp.get("password"),
        "primaryEmail": data_temp.get("account"), # 完整的Gsuite账号 前缀+@+域名
        "changePasswordAtNextLogin": True, # 下次登入时修改密码
        "orgUnitPath": data_temp.get("orgUnit") # 用户组
    }

```

### 说明

由于之前不会用Oauth2 所以直接用了Google的sdk 所以效率是真的不行。一个请求1s 起码的，贫瘠在构建服务那。
现在会Oauth2的基本使用了 ，有空再重构吧。
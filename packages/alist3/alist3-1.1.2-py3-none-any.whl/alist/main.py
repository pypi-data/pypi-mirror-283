# pylint:disable=W0707
import requests
import hashlib
import json
import os.path
import sys
import pickle
import base64
import warnings

from platform import platform
from urllib.parse import quote
from typing import Union
from urllib.parse import urljoin

from . import error, file, folder, utils


class AListUser:
    def __init__(self, username: str, password: str='', otp_code=None):
        """
        AList用户类

        Args:
            username (str): AList的用户名
            password (str): AList的密码
            otp_code (str): OTP

        """
        self.un = username
        self.rawpwd = password
        self.pwd = ''
        self.oc = otp_code
        
        sha = hashlib.sha256()
        sha.update(self.rawpwd.encode())
        sha.update(b"-https://github.com/alist-org/alist")
        self.pwd = sha.hexdigest()
        

    def dump(self,fp, rawpwd=False):
        data = {
            'username':base64.b64encode(self.un.encode()),
            'pwd':base64.b64encode(self.pwd.encode())
        }
        if rawpwd:
            warnings.warn('保存明文密码至文件是不安全的',error.SecurityWarning)
            data['raw'] = base64.b64encode(self.rawpwd.encode())
        
        pickle.dump(data,fp)
    
    def dumps(self, rawpwd=False):
        data = {
            'username':base64.b64encode(self.un.encode()),
            'pwd':base64.b64encode(self.pwd.encode())
        }
        if rawpwd:
            warnings.warn('保存明文密码至文件是不安全的',error.SecurityWarning)
            data['raw'] = base64.b64encode(self.rawpwd.encode())
        
        return pickle.dumps(data)
        

class AList:
    def __init__(self, endpoint: str, test=True):
        """
        AList的SDK，此为主类。

        Args:
            endpoint (str):AList地址
        """
        if "http" not in endpoint:
            raise ValueError(endpoint + "不是有效的uri")

        self.endpoint = endpoint  # alist地址
        self.token = ""  # JWT Token

        # 构建UA
        ver = [
            str(sys.version_info.major),
            str(sys.version_info.minor),
            str(sys.version_info.micro),
        ]
        ver = ".".join(ver)
        pf = platform().split("-")

        self.headers = {
            "User-Agent": f"AListSDK/1.1.2 (Python{ver};{pf[3]}) {pf[0]}/{pf[1]}",
            "Content-Type": "application/json",
            "Authorization": "",
        }
        
        if test:
            self.Test()
        
    def _isBadRequest(self, r, msg):
        # 是否为不好的请求
        try:
            j = json.loads(r.text)

        except json.JSONDecodeError:

            raise ValueError("服务器返回的数据不是JSON数据")

        if j["code"] != 200:
            raise error.ServerError(msg + ":" + j["message"])

    def _getURL(self, path):
        # 获取api端点
        return urljoin(self.endpoint, path)

    def _parserJson(self, js):
        return utils.ToClass(json.loads(js))
    
    def Test(self):
        try:
            res = requests.get(self._getURL('/ping'),headers=self.headers)
        except:
            return False
            
        if res.text != 'pong':
            return False
        return True
            
    def Login(self, user: AListUser):
        """
        登录

        Args:
            user (AListUser): AList用户

        Returns:
            (bool): 是否成功


        """
        password = user.pwd
        username = user.un
        otp_code = user.oc
        URL = self._getURL("/api/auth/login/hash")

        # 构建json数据
        data = {"username": username, "password": password, "otp_code": otp_code}
        data = json.dumps(data)

        r = requests.post(URL, headers=self.headers, data=data)
        # 处理返回数据
        self._isBadRequest(r, "账号或密码错误")
        # 保存
        self.token = json.loads(r.text)["data"]["token"]
        self.headers["Authorization"] = self.token
        return True

    def UserInfo(self):
        """
        获取当前登录的用户的信息

        Returns:
            (dict):一个字典，包含了当前用户的信息。

        """

        URL = self._getURL("/api/me")
        r = requests.get(URL, headers=self.headers)
        return self._parserJson(r.text).data

    def ListDir(
        self,
        path: Union[str, folder.AListFolder],
        page: int = 1,
        per_page: int = 50,
        refresh: bool = False,
        password: str = "",
    ):
        """
        列出指定目录下的所有文件或文件夹。

        Args:
            path (str,AListFolder): 需要列出的目录
            page (int): 页数
            per_page (int): 每页的数量
            refresh (bool): 是否强制刷新
            password (str): 目录密码

        Returns:
            (generator):指定目录下的文件

        """

        URL = self._getURL("/api/fs/list")

        data = json.dumps(
            {
                "path": str(path),
                "password": password,
                "page": page,
                "per_page": per_page,
                "refresh": refresh,
            }
        )
        r = requests.post(URL, data=data, headers=self.headers)
        self._isBadRequest(r, "上传失败")

        for item in json.loads(r.text)["data"]["content"]:
            i = {"path": os.path.join(str(path), item["name"]), "is_dir": item["is_dir"]}
            yield utils.ToClass(i)

    def open(
        self, path: Union[str, folder.AListFolder, file.AListFile], password: str = ""
    ):
        """
        打开文件/文件夹

        Args:
            path (str, AListFolder, AListFile): 路径
            password (str): 密码

        Returns:
            (AListFolder): AList目录对象
            (AListFile): AList文件对象


        """

        URL = self._getURL("/api/fs/get")

        data = json.dumps({"path": str(path), "password": password})
        r = requests.post(URL, headers=self.headers, data=data)

        rjson = json.loads(r.text)
        if rjson["data"]["is_dir"]:
            return folder.AListFolder(str(path), rjson["data"])
        else:
            return file.AListFile(str(path), rjson["data"])

    def Mkdir(self, path: str):
        """
        创建文件夹

        Args:
            path (str): 要创建的目录

        Returns:
            (bool): 是否成功


        """
        URL = self._getURL("/api/fs/mkdir")
        data = json.dumps({"path": path})

        r = requests.post(URL, data=data, headers=self.headers)
        self._isBadRequest(r, "创建失败")

        return True

    def Upload(self, path: Union[str, file.AListFile], local: str):
        """
        上传文件

        Args:
            path (str, AListFile): 上传的路径
            locel (str): 本地路径

        Returns:
            (bool): 是否成功


        """
        URL = self._getURL("/api/fs/put")

        files = open(local, "rb").read()
        FilePath = quote(str(path))

        headers = self.headers.copy()
        headers["File-Path"] = FilePath
        headers["Content-Length"] = str(len(files))
        del headers["Content-Type"]

        r = requests.put(URL, data=files, headers=headers)
        self._isBadRequest(r, "上传失败")

        return True

    def Rename(self, src: Union[str, folder.AListFolder, file.AListFile], dst: str):
        """
        重命名

        Args:
            src (str, AListFolder, AListFile): 原名
            dst (str): 要更改的名字

        Returns:
            (bool): 是否成功


        """
        URL = self._getURL("/api/fs/rename")

        data = json.dumps({"path": str(src), "name": dst})

        r = requests.post(URL, headers=self.headers, data=data)
        self._isBadRequest(r, "重命名失败")
        return True

    def Remove(self, path: Union[str, file.AListFile]):
        URL = self._getURL("/api/fs/remove")
        payload = json.dumps(
            {"names": [str(os.path.basename(str(path)))], "dir": str(os.path.dirname(str(path)))}
        )

        r = requests.post(URL, data=payload, headers=self.headers)
        self._isBadRequest(r, "删除失败")
        return True

    def RemoveFolder(self, path: Union[str, folder.AListFolder]):
        URL = self._getURL("/api/fs/remove_empty_directory")
        data = json.dumps({"src_dir": str(path)})
        r = requests.post(URL, data=data, headers=self.headers)
        self._isBadRequest(r, "删除失败")
        return True

    def Copy(
        self, src: Union[str, file.AListFile], dstDir: Union[str, folder.AListFolder]
    ):
        URL = self._getURL("/api/fs/copy")
        data = json.dumps(
            {
                "src_dir": os.path.dirname(str(src)),
                "dst_dir": str(dstDir),
                "names": [os.path.basename(str(src))],
            }
        )
        r = requests.post(URL, data=data, headers=self.headers)
        self._isBadRequest(r, "复制失败")
        return True

    def Move(
        self, src: Union[str, file.AListFile], dstDir: Union[str, folder.AListFolder]
    ):
        URL = self._getURL("/api/fs/move")
        data = json.dumps(
            {
                "src_dir": os.path.dirname(str(src)),
                "dst_dir": str(dstDir),
                "names": [os.path.basename(str(src))],
            }
        )
        r = requests.post(URL, data=data, headers=self.headers)
        self._isBadRequest(r, "移动失败")
        return True

    def SiteConfig(self):
        url = self._getURL("/api/public/settings")
        r = requests.get(url, headers=self.headers)
        self._isBadRequest(r, "AList配置信息获取失败")
        return self._parserJson(r.text).data


class AListAdmin(AList):
    def __init__(self, user, endpoint):
        super().__init__(endpoint)
        self.Login(user)
        if self.UserInfo().id != 1:
            raise error.AuthenticationError("无权限")

    def ListMeta(self, page=None, per_page=None):
        url = self._getURL("/api/admin/meta/list")
        prams = {"page": page, "per_page": per_page}
        r = requests.get(url, params=prams, headers=self.headers)
        self._isBadRequest(r, "无法列出元数据")
        return self._parserJson(r.text)
    
    def GetMeta(self, idx):
        url = self._getURL('/api/admin/meta/get')
        r = requests.get(url, params={'id':idx},headers=self.headers)
        self._isBadRequest(r, '无法找到该元数据')


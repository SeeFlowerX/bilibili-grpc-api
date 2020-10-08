'''
作者: weimo
创建日期: 2020-10-08 15:57:01
上次编辑时间: 2020-10-08 21:22:14
一个人的命运啊,当然要靠自我奋斗,但是...
'''

class Config(object):

    def __init__(self):
        self.dalvik_ver = "2.1.0"
        self.os_ver = "9"
        self.brand = "Xiaomi"
        self.model = "MIUI/V10.3.17.0.PFKCNXM"
        self.app_ver = "6.7.0"
        self.build = 6070600
        self.channel = "bilibili140"
        self.network_type = 1 # wifi
        self.network_tf = 0
        self.network_oid = "46007"
        self.cronet = "1.21.0"
        self.auth = ""
        self.buvid = ""
        self.mobiApp = "android"
        self.platform = "android"
        self.env = "prod"
        self.appId = 1
        self.region = "CN"
        self.language = "zh"

    @staticmethod
    def get_user_agent():
        c = Config()
        user_agent = (
            f"Dalvik/{c.dalvik_ver} "
            f"(Linux; U; Android {c.os_ver}; {c.brand} {c.model}) {c.app_ver} "
            f"os/android model/{c.model} mobi_app/android build/{c.build} "
            f"channel/{c.channel} innerVer/{c.build} osVer/{c.os_ver} "
            f"network/{c.network_type} grpc-java-cronet/{c.cronet}"
        )
        return user_agent
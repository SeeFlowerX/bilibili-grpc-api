'''
作者: weimo
创建日期: 2020-10-08 15:57:01
上次编辑时间: 2020-10-09 15:45:39
一个人的命运啊,当然要靠自我奋斗,但是...
'''
import base64

from google.protobuf.reflection import GeneratedProtocolMessageType

from header.fawkesreq_pb2 import FawkesReq
from header.metadata_pb2 import Metadata
from header.device_pb2 import Device
from header.network_pb2 import Network
from header.restriction_pb2 import Restriction
from header.locale_pb2 import Locale

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

    def serialize_base64(self, msg: GeneratedProtocolMessageType):
        return base64.b64encode(msg.SerializeToString()).decode("utf-8").rstrip("=")

    def get_fawkesreq_bin(self):
        msg = FawkesReq() # type: GeneratedProtocolMessageType
        msg.appkey = self.mobiApp
        msg.env = self.env
        return self.serialize_base64(msg)

    def get_metadata_bin(self):
        msg = Metadata() # type: GeneratedProtocolMessageType
        msg.accessKey = self.auth
        msg.mobiApp = self.mobiApp
        # 没有的值不要做操作
        # msg.device = ""
        msg.build = self.build
        msg.channel = self.channel
        msg.buvid = self.buvid
        msg.platform = self.platform
        return self.serialize_base64(msg)

    def get_device_bin(self):
        msg = Device() # type: GeneratedProtocolMessageType
        msg.appId = self.appId;
        msg.build = self.build;
        msg.buvid = self.buvid;
        msg.mobiApp = self.mobiApp;
        msg.platform = self.platform;
        msg.channel = self.channel;
        msg.brand = self.brand;
        msg.model = self.model;
        msg.osver = self.os_ver;
        return self.serialize_base64(msg)

    def get_network_bin(self):
        msg = Network() # type: GeneratedProtocolMessageType
        msg.type = self.network_type;
        msg.oid = self.network_oid;
        return self.serialize_base64(msg)

    def get_restriction_bin(self):
        # restriction 也就是限制的意思 最好什么都没有 所以这里不进行任何设置
        msg = Restriction() # type: GeneratedProtocolMessageType
        # msg.teenagersMode = False;
        # msg.lessonsMode = False;
        # msg.mode = 0;
        # msg.review = False;
        return self.serialize_base64(msg)

    def get_locale_bin(self):
        msg = Locale() # type: GeneratedProtocolMessageType
        msg.cLocale.language = self.language;
        msg.cLocale.region = self.region;
        msg.sLocale.language = self.language;
        msg.sLocale.region = self.region;
        return self.serialize_base64(msg)

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
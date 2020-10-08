'''
作者: weimo
创建日期: 2020-10-08 15:44:34
上次编辑时间: 2020-10-08 21:24:48
一个人的命运啊,当然要靠自我奋斗,但是...
'''
import gzip
import base64
import struct
import requests

from io import BytesIO
from google.protobuf.reflection import GeneratedProtocolMessageType
from google.protobuf.json_format import MessageToDict

from header.fawkesreq_pb2 import FawkesReq
from header.metadata_pb2 import Metadata
from header.device_pb2 import Device
from header.network_pb2 import Network
from header.restriction_pb2 import Restriction
from header.locale_pb2 import Locale
from payload.playviewreq_pb2 import PlayViewReq

from service.config import Config

CLEAR_GZIP_HEADER = bytes([31, 139, 8, 0, 0, 0, 0, 0, 0, 0])

class Video(object):

    def __init__(self):
        self.url = "https://grpc.biliapi.net/bilibili.pgc.gateway.player.v1.PlayURL/PlayView"
        self.config = Config()

    def get_headers(self):
        headers = {
            "user-agent": self.config.get_user_agent(),
            "content-type": "application/grpc",
            "te": "trailers",
            "x-bili-fawkes-req-bin": self.get_fawkesreq_bin(),
            "x-bili-metadata-bin": self.get_metadata_bin(),
            "authorization": f"identify_v1 {self.config.auth}",
            "x-bili-device-bin": self.get_device_bin(),
            "x-bili-network-bin": self.get_network_bin(),
            "x-bili-restriction-bin": "",
            "x-bili-locale-bin": self.get_locale_bin(),
            "grpc-encoding": "gzip",
            "grpc-accept-encoding": "identity,gzip",
            "grpc-timeout": "17985446u" # u指微秒 -> us
        }
        return headers

    def add_payload_header(self, payload: bytes):
        # 大端默认值1 所以是b
        # payload长度为long 所以是l
        # https://docs.python.org/zh-cn/3/library/struct.html
        return struct.pack("!bl", 1, len(payload)) + payload

    def gzip_decompress(self, msg: bytes):
        # 用于测试抓包数据
        for offset in range(len(msg)):
            if msg[offset] == 0x1f:
                msg = msg[offset:]
                break
        compressed = gzip.GzipFile(fileobj=BytesIO(msg))
        return compressed.read()

    def gzip_compress(self, msg: GeneratedProtocolMessageType):
        compressed = gzip.compress(msg.SerializeToString())
        # 注意更换gzip的header
        compressed = CLEAR_GZIP_HEADER + compressed[10:]
        return compressed

    def serialize_base64(self, msg: GeneratedProtocolMessageType):
        return base64.b64encode(msg.SerializeToString()).decode("utf-8").rstrip("=")

    def get_fawkesreq_bin(self):
        msg = FawkesReq() # type: GeneratedProtocolMessageType
        msg.appkey = self.config.mobiApp
        msg.env = self.config.env
        return self.serialize_base64(msg)

    def get_metadata_bin(self):
        msg = Metadata() # type: GeneratedProtocolMessageType
        msg.accessKey = self.config.auth
        msg.mobiApp = self.config.mobiApp
        # 没有的值不要做操作
        # msg.device = ""
        msg.build = self.config.build
        msg.channel = self.config.channel
        msg.buvid = self.config.buvid
        msg.platform = self.config.platform
        return self.serialize_base64(msg)

    def get_device_bin(self):
        msg = Device() # type: GeneratedProtocolMessageType
        msg.appId = self.config.appId;
        msg.build = self.config.build;
        msg.buvid = self.config.buvid;
        msg.mobiApp = self.config.mobiApp;
        msg.platform = self.config.platform;
        msg.channel = self.config.channel;
        msg.brand = self.config.brand;
        msg.model = self.config.model;
        msg.osver = self.config.os_ver;
        return self.serialize_base64(msg)

    def get_network_bin(self):
        msg = Network() # type: GeneratedProtocolMessageType
        msg.type = self.config.network_type;
        msg.oid = self.config.network_oid;
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
        msg.cLocale.language = self.config.language;
        msg.cLocale.region = self.config.region;
        msg.sLocale.language = self.config.language;
        msg.sLocale.region = self.config.region;
        return self.serialize_base64(msg)

    def get_payload(self, epid: int, cid: int, qn: int = 112, **kwargs):
        # 为0或者False 不做操作
        msg = PlayViewReq()
        msg.epId = epid
        msg.cid = cid
        msg.qn = qn
        # msg.fnver = kwargs["fnver"] if kwargs.get("fnver") else 0
        msg.fnval = kwargs["fnval"] if kwargs.get("fnval") else 16
        # msg.download = kwargs["download"] if kwargs.get("download") else 0
        # msg.forceHost = kwargs["forceHost"] if kwargs.get("forceHost") else 0
        msg.fourk = kwargs["fourk"] if kwargs.get("fourk") else True
        msg.spmid = kwargs["spmid"] if kwargs.get("spmid") else "pgc.pgc-video-detail.0.0"
        msg.fromSpmid = kwargs["fromSpmid"] if kwargs.get("fromSpmid") else "search.search-result.0.0"
        # msg.teenagersMode = kwargs["teenagersMode"] if kwargs.get("teenagersMode") else 0
        msg.preferCodecType = kwargs["preferCodecType"] if kwargs.get("preferCodecType") else 2
        msg.isPreview = kwargs["isPreview"] if kwargs.get("isPreview") else False # type: bool
        # msg.roomId = kwargs["roomId"] if kwargs.get("roomId") else 0
        # print(MessageToDict(msg)) # 可以输出检查一下
        return self.gzip_compress(msg)

    def parse_payload(self, payload: bytes):
        # 用于测试解析抓包的payload
        payload = self.gzip_decompress(payload)
        msg = PlayViewReq()
        msg.ParseFromString(payload)
        print(MessageToDict(msg))

    def request(self, epid: int, cid: int, qn: int = 112):
        headers = self.get_headers()
        payload = self.get_payload(epid, cid, qn)
        payload = self.add_payload_header(payload)
        try:
            r = requests.post(self.url, data=payload, headers=headers, timeout=5)
        except Exception as e:
            print(f"error --> {e}")
            return
        print(r.content)
        return r.content
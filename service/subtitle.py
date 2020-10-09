'''
作者: weimo
创建日期: 2020-10-09 13:47:36
上次编辑时间: 2020-10-09 15:35:13
一个人的命运啊,当然要靠自我奋斗,但是...
'''
import gzip
import base64
import struct
import requests

from io import BytesIO
from google.protobuf.reflection import GeneratedProtocolMessageType
from google.protobuf.json_format import MessageToDict

from payload.dmviewreq_pb2 import DmViewReq
from service.config import Config
from service.service import Service

class Subtitle(Service):

    def __init__(self):
        super(Subtitle, self).__init__()
        self.url = "https://app.bilibili.com/bilibili.community.service.dm.v1.DM/DmView"
        self.config = Config()

    def get_headers(self):
        headers = {
            "env": "prod",
            "app-key": "android",
            "user-agent": self.config.get_user_agent(),
            "x-bili-metadata-bin": self.config.get_metadata_bin(),
            "authorization": f"identify_v1 {self.config.auth}",
            "x-bili-device-bin": self.config.get_device_bin(),
            "x-bili-network-bin": self.config.get_network_bin(),
            "x-bili-restriction-bin": "",
            "x-bili-locale-bin": self.config.get_locale_bin(),
            "x-bili-fawkes-req-bin": self.config.get_fawkesreq_bin(),
            "content-type": "application/grpc",
            "accept-encoding": "gzip",
            "cookie": "bfe_id=; sid="
        }
        return headers

    def parse_payload(self, payload: bytes):
        # 用于测试解析抓包的payload
        msg = DmViewReq()
        msg.ParseFromString(self.slice_message(payload))
        return MessageToDict(msg)

    def parse_reply(self, resp: bytes):
        try:
            import json
            import pathlib
            from response.dmviewreply_pb2 import DmViewReply
        except Exception as e:
            return
        reply = DmViewReply()
        reply.ParseFromString(resp)
        path = pathlib.Path("subtitle_resp.json")
        # MessageToJson直接就是字符串了 但是中文会乱码 还是手动转一下
        text = json.dumps(MessageToDict(reply), ensure_ascii=False, indent=4)
        path.write_text(text, encoding="utf-8")

    def get_payload(self, pid: int, oid: int, stype: int = 1):
        msg = DmViewReq()
        msg.pid = pid
        msg.oid = oid
        msg.type = stype
        print(MessageToDict(msg)) # 可以输出检查一下
        return self.add_payload_header(msg.SerializeToString(), compressed=False)

    def request(self, pid: int, oid: int, stype: int = 1):
        headers = self.get_headers()
        payload = self.get_payload(pid, oid, stype)
        # print([hex(_)[2:].zfill(2).upper() for _ in list(payload)])
        try:
            r = requests.post(self.url, data=payload, headers=headers, timeout=5)
        except Exception as e:
            print(f"error --> {e}")
            return
        resp = self.slice_message(r.content)
        self.parse_reply(resp)
        return resp
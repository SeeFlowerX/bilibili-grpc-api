'''
作者: weimo
创建日期: 2020-10-08 15:44:34
上次编辑时间: 2020-10-09 14:52:13
一个人的命运啊,当然要靠自我奋斗,但是...
'''

import requests
from google.protobuf.json_format import MessageToDict

from payload.playviewreq_pb2 import PlayViewReq
from service.config import Config
from service.service import Service

class Video(Service):

    def __init__(self):
        super(Video, self).__init__()
        self.url = "https://grpc.biliapi.net/bilibili.pgc.gateway.player.v1.PlayURL/PlayView"
        self.config = Config()

    def get_headers(self):
        headers = {
            "user-agent": self.config.get_user_agent(),
            "content-type": "application/grpc",
            "te": "trailers",
            "x-bili-fawkes-req-bin": self.config.get_fawkesreq_bin(),
            "x-bili-metadata-bin": self.config.get_metadata_bin(),
            "authorization": f"identify_v1 {self.config.auth}",
            "x-bili-device-bin": self.config.get_device_bin(),
            "x-bili-network-bin": self.config.get_network_bin(),
            "x-bili-restriction-bin": "",
            "x-bili-locale-bin": self.config.get_locale_bin(),
            "grpc-encoding": "gzip",
            "grpc-accept-encoding": "identity,gzip",
            "grpc-timeout": "17985446u" # u指微秒 -> us
        }
        return headers

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
        return self.add_payload_header(self.gzip_compress_proto_message(msg))

    def parse_reply(self, resp: bytes):
        try:
            import json
            import pathlib
            from response.playviewreply_pb2 import PlayViewReply
        except Exception as e:
            return
        reply = PlayViewReply()
        reply.ParseFromString(resp)
        path = pathlib.Path("video_resp.json")
        # MessageToJson直接就是字符串了 但是中文会乱码 还是手动转一下
        text = json.dumps(MessageToDict(reply), ensure_ascii=False, indent=4)
        path.write_text(text, encoding="utf-8")

    def parse_payload(self, payload: bytes):
        # 用于测试解析抓包的payload
        payload = self.slice_message(payload)
        msg = PlayViewReq()
        msg.ParseFromString(payload)
        return MessageToDict(msg)

    def request(self, epid: int, cid: int, qn: int = 112):
        headers = self.get_headers()
        payload = self.get_payload(epid, cid, qn)
        try:
            r = requests.post(self.url, data=payload, headers=headers, timeout=5)
        except Exception as e:
            print(f"error --> {e}")
            return
        resp = self.slice_message(r.content)
        self.parse_reply(resp)
        return resp
'''
作者: weimo
创建日期: 2020-10-09 14:03:54
上次编辑时间: 2020-10-09 15:04:28
一个人的命运啊,当然要靠自我奋斗,但是...
'''

import gzip
import base64
import struct

from io import BytesIO
from google.protobuf.reflection import GeneratedProtocolMessageType

CLEAR_GZIP_HEADER = bytes([31, 139, 8, 0, 0, 0, 0, 0, 0, 0])

class Service(object):

    def add_payload_header(self, payload: bytes, compressed: bool = True):
        # 压缩的为大端 大端值1 所以是b
        # payload长度为long 所以是l
        # https://docs.python.org/zh-cn/3/library/struct.html
        endian = 1 if compressed else 0
        return struct.pack("!bl", endian, len(payload)) + payload

    def gzip_compress_proto_message(self, msg: GeneratedProtocolMessageType):
        # 压缩protobuf编码后的数据
        compressed = gzip.compress(msg.SerializeToString())
        # 替换gzip的header
        compressed = CLEAR_GZIP_HEADER + compressed[10:]
        return compressed

    def gzip_compress(self, msg: bytes):
        # 压缩数据
        compressed = gzip.compress(msg)
        # 替换gzip的header
        compressed = CLEAR_GZIP_HEADER + compressed[10:]
        return compressed

    def gzip_decompress(self, msg: bytes):
        compressed = gzip.GzipFile(fileobj=BytesIO(msg))
        return compressed.read()

    def slice_message(self, msg: bytes):
        # 提取message
        byteorder, length = struct.unpack("!bl", msg[:5])
        if byteorder == 0x01:
            # 一般需要gzip解压
            return self.gzip_decompress(msg[5:])
        return msg[5:5+length]
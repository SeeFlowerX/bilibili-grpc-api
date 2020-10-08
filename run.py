'''
作者: weimo
创建日期: 2020-10-08 16:28:00
上次编辑时间: 2020-10-08 21:21:32
一个人的命运啊,当然要靠自我奋斗,但是...
'''
import pathlib
from service.video import Video

def test_payload():
    # 测试本地文件
    path = pathlib.Path(r"test\req.bin")
    payload = path.read_bytes()
    vins = Video()
    vins.parse_payload(payload)

def main():
    epid = 341988
    cid = 240156492
    ins = Video()
    resp = ins.request(epid, cid, qn=120)

if __name__ == "__main__":
    main()
    # test_payload()
    
# python -m grpc_tools.protoc -I header --python_out=header header\metadata.proto
# python -m grpc_tools.protoc -I header --decode Metadata metadata.proto < test.bin
# https://stackoverflow.com/questions/35049657/how-to-decode-binary-raw-google-protobuf-data
# https://developers.google.com/protocol-buffers/docs/proto
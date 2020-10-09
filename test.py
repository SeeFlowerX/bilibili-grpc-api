'''
作者: weimo
创建日期: 2020-10-09 14:34:19
上次编辑时间: 2020-10-09 14:39:25
一个人的命运啊,当然要靠自我奋斗,但是...
'''

import sys
import json
import pathlib
from service.video import Video
from service.subtitle import Subtitle

def format_print(msg: dict):
    print(json.dumps(msg, ensure_ascii=False, indent=4))

def test_subtitle_payload():
    path = pathlib.Path(r"test\subtitle_req.bin")
    subtitle = Subtitle()
    return subtitle.parse_payload(path.read_bytes())

def test_video_payload():
    path = pathlib.Path(r"test\video_req.bin")
    video = Video()
    return video.parse_payload(path.read_bytes())

if __name__ == "__main__":
    if len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print("test example:\npython test.py -t video")
    elif len(sys.argv) == 3 and sys.argv[1] == "-t":
        if sys.argv[2] == "subtitle":
           format_print(test_subtitle_payload())
        if sys.argv[2] == "video":
            format_print(test_video_payload())
    else:
        sys.exit("params error, use -h plz.")
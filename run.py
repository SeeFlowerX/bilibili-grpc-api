'''
作者: weimo
创建日期: 2020-10-08 16:28:00
上次编辑时间: 2020-10-09 15:35:33
一个人的命运啊,当然要靠自我奋斗,但是...
'''
import sys

from service.video import Video
from service.subtitle import Subtitle

def subtitle():
    pid = 712346749
    oid = 240156492
    resp = Subtitle().request(pid, oid, stype=1)
    print(resp)

def video():
    epid = 342547
    cid = 239158825
    resp = Video().request(epid, cid, qn=120)
    print(resp)

if __name__ == "__main__":
    video()
    subtitle()
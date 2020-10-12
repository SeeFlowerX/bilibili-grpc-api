# bilibili grpc api

bilibili grpc相关的api请求，仅作研究学习。

鉴权参数：identify_v1和buvid，如需使用请在config.py中设置。

# 使用

## proto文件生成py文件

> python -m grpc_tools.protoc -I header --python_out=header header\metadata.proto

## 指定proto文件解码

> python -m grpc_tools.protoc -I header --decode Metadata metadata.proto < test.bin

## 测试解析payload

> python test.py -t video

```json
{
    "epId": "341988",
    "cid": "240156492",
    "qn": "120",
    "fnval": 16,
    "fourk": true,
    "spmid": "pgc.pgc-video-detail.0.0",
    "fromSpmid": "default-value",
    "preferCodecType": "CODE265"
}
```

> python test.py -t subtitle

```json
{
    "pid": "712346749",
    "oid": "240156492",
    "type": 1
}
```

## 测试请求视频

> python run.py

# 解析效果

原理详见：[哔哩哔哩视频和字幕接口分析](https://blog.seeflower.dev/explore-bilibili-video-grpc-request/)，欢迎指正不足之处。

返回数据proto文件构成复杂，有需要可以参考上面的文章自行编写proto文件。

- 视频请求和返回解析

![视频请求payload解析效果](/images/video_req_1.png)
![视频请求返回解析效果](/images/video_resp.png)
![视频请求返回解析效果-末尾](/images/video_resp_2.png)

- 字幕请求返回解析

![字幕请求返回解析](/images/subtitle_resp.png)

# 参考

- https://developers.google.com/protocol-buffers/docs/proto
- https://stackoverflow.com/questions/35049657/how-to-decode-binary-raw-google-protobuf-data
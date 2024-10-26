import urllib.request
import json
import re
import requests
from lxml import html
from bs4 import BeautifulSoup


# 加载json
with open('1729955282709.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 批量处理
for x in data:
    try:
        # 取发布时间
        created_at = x["created_at"]
        # print(created_at[:11])

        # 取幕后视频数据对象(srt)
        srt_value = x["metadata"]["card"]["legacy"]["binding_values"][0]["value"]["string_value"]
        # print(first_object["metadata"]["card"]["legacy"]["binding_values"][0]["value"]["string_value"])
        # 处理多余的反斜杠、引号
        srt_value_cleaned = re.sub(r'\\+', r'\\', srt_value).replace('\\\"', '\"')
        # json读取
        json_data = json.loads(srt_value_cleaned)

        # 获取跳转链接url
        url = json_data["destination_objects"]["browser_with_docked_media_1"]["data"]["url_data"]["url"]
        # print(media_id)
        # 请求跳转链接获取标题并优化
        title = BeautifulSoup(requests.get(url.split('?')[0]).text, 'html.parser').title.string.split('|')[0].strip()
        # 输出发布日期年月日以及标题
        print(created_at[:11] + title)

        # 获取第一个媒体实体的 ID
        media_id = next(iter(json_data['media_entities']))
        # 找到最大 bitrate 的 video
        variants = json_data['media_entities'][media_id]['video_info']['variants']
        max_bitrate_variant = max((v for v in variants if 'bitrate' in v), key=lambda x: x['bitrate'])['url']
        # 输出视频链接
        print(max_bitrate_variant)

    # json读取异常
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
    # 缺值异常
    except KeyError as e:
        print(f"KeyError: {e} - 跳过此项")

import requests
import json
import urllib.request
import os
import argparse


def download_canvas(authorization, trackId):
    headers = {
        'authorization': authorization,
    }

    params = {
        'operationName': 'canvas',
        'variables': json.dumps({"uri": f"spotify:track:{trackId}"}),
        'extensions': json.dumps({
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "1b1e1915481c99f4349af88268c6b49a2b601cf0db7bca8749b5dd75088486fc"
            }
        }),
    }

    re = requests.get('https://api-partner.spotify.com/pathfinder/v1/query', params=params, headers=headers)

    try:
        url = json.loads(re.text)['data']['trackUnion']['canvas']['url']
        name = url.split('/')[-1]

        if not os.path.exists(name):
            urllib.request.urlretrieve(url, name)
            print(f"下载成功. {name}")
        else:
            print(f"文件已存在.")
    except:
        print("存在未知错误.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='下载Spotify的Canvas.')
    # parser.add_argument('trackId', type=str, help='输入歌曲的id.')
    parser.add_argument('url', type=str, help='输入歌曲的分享链接.')
    parser.add_argument('-auth', type=str, help='输入Authorization.（1小时过期）')

    args = parser.parse_args()
    url = args.url.split('/')[-1].split('?')[0]
    # if args.trackId is None:
    download_canvas(args.auth, url)
    # elif args.url is None:
    #     download_canvas(args.authorization, args.trackId)
    # else:
    #     print('缺少必填字段')

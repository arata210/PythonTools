import requests
import json
import urllib.request
import os
import argparse
from bs4 import BeautifulSoup


def spotify_auth(url, sp_dc):
    cookies = {'sp_dc': sp_dc}
    re = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(re.text, 'html.parser')

    # 查找包含accessToken的script标签
    session = soup.find(id='session')

    # 提取accessToken
    access_token = None
    for script in session:
        try:
            # 转换为字典
            data = json.loads(script.string)
            if 'accessToken' in data:
                access_token = data['accessToken']
                break
        except (ValueError, TypeError):
            continue

    if access_token:
        return access_token
    else:
        return False


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
        print(name)

        if not os.path.exists(name):
            urllib.request.urlretrieve(url, name)
            print(f"下载成功. {name}")
        else:
            print(f"文件已存在.")
    except:
        print("存在未知错误.")
        # print("未登录Cookies/文件路径错误/该音乐暂无Canvas/文件无法正常下载/链接错误")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Spotify Canvas Downloader', description='下载Spotify的Canvas.')
    parser.add_argument('url', type=str, help='输入歌曲的分享链接.')
    # parser.add_argument('-o', type=str, help='输出目录.')
    parser.add_argument('-cookie', type=str, help='Cookies中sp_dc的值.')
    # parser.add_argument('-trackId', type=str, help='输入歌曲的id.')
    # parser.add_argument('-auth', type=str, help='输入Authorization.（1小时过期）')

    args = parser.parse_args()
    spotify_auth = spotify_auth(args.url, args.cookie)
    if spotify_auth:
        auth = 'Bearer ' + spotify_auth
    else:
        print('auth获取失败')
    # print(auth)
    trackId_from_url = args.url.split('/')[-1].split('?')[0]
    print(trackId_from_url)
    download_canvas(auth, trackId_from_url)

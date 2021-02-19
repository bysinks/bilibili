import requests
import re,sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
}


def video_name(url):
    name = requests.get(url, headers=header).json()
    names = name['data'][0]['part']
    cid = name['data'][0]['cid']
    return names,cid

def get_video(id,url):
    head = {
        "Range": "",
        "Host": "",
        "origin":"https://www.bilibili.com",
        "Referer": "https://www.bilibili.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
    }
    c=str(video_name(url)[1])
    u='https://api.bilibili.com/x/player/playurl?cid=%s&bvid=%s&qn=64&type=&otype=json'%(c,id)
    contents=requests.get(u,headers=header).json()
    data=contents['data']['durl'][0]['url']
    data1=contents['data']['durl'][0]['size']
    flv_host = re.findall("https://(.*)com", data, re.I)
    print(data)
    print(flv_host[0]+'com')
    head["Host"] = flv_host[0]+'com'
    head["Range"]="bytes=0-%s"%data1
    res = requests.get(data, headers=head, stream=True, verify=False)
    name = video_name(url)[0]
    chunk_size = 1024
    with open("{name}.mp4".format(name=name), "wb") as f:
        for i in res.iter_content(chunk_size):
            f.write(i)
    print("视频地址：", data + "\n", "大小：", data1)

def get_fanju(id,url):
    head = {
        "Range": "",
        "Host": "",
        "origin":"https://www.bilibili.com",
        "Referer": "https://www.bilibili.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
    }
    contents=requests.get(url,headers=header).json()
    data=contents['result']['durl'][0]['backup_url'][0]
    data1=contents['result']['durl'][0]['size']
    flv_host = re.findall("https://(.*)com", data, re.I)
    print(flv_host[0] + 'com')
    print(data)
    head["Host"] = flv_host[0]+'com'
    head["Range"]="bytes=0-%s"%data1
    res = requests.get(data, headers=head, stream=True, verify=False)
    name = 'test'
    chunk_size = 1024
    with open("{name}.flv".format(name=name), "wb") as f:
        for i in res.iter_content(chunk_size):
            f.write(i)
    print("视频地址：", data + "\n", "大小：", data1)

if __name__ == '__main__':
    sp_helps = """python3 -v bvid  普通视频爬取
    python3 -f epid  番剧视频爬取(不含大会员)"""
    id = sys.argv[1:3]
    try:
        try:
            if id[0] == "-v":
                video_api = "https://api.bilibili.com/x/player/pagelist?bvid=%s&jsonp=jsonp" % id[1]
                get_video(id=id[1], url=video_api)
            elif id[0] == "-f":
                fanju_api = "https://api.bilibili.com/pgc/player/web/playurl?ep_id=%s&jsonp=jsonp" % id[1]
                get_fanju(id[1], fanju_api)
            elif id[0] == "-h" or id[0] == "--help":
                print(sp_helps)
        except:
            print("可能视频需要大会员或者有权限控制")
    except:
        print("python3 -h OR --help 查看用法")


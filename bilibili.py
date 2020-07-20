import requests
import json
import re
from bs4 import BeautifulSoup
from sys import argv

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
}


def video_name(id):
    url = "https://api.bilibili.com/x/player/pagelist?bvid=" + id + "&jsonp=jsonp"
    video_logo = requests.get(url, headers=header)
    video_name = video_logo.text
    name = json.loads(video_name)
    names = name['data'][0]['part']
    return names

def video_cid(id):
    url = "https://api.bilibili.com/x/player/pagelist?bvid=" + id + "&jsonp=jsonp"
    video_logo = requests.get(url, headers=header)
    video_name = video_logo.text
    name = json.loads(video_name)
    cid = name['data'][0]['cid']
    return cid

def get_flv(id):
    head = {
        "host": "",
        "Referer": "https://www.bilibili.com",
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;WOW64) AppleWebKit/537.36(KHTML,likeGecko)Chrome/63.0.3239.132Safari/537.36"
    }
    c=str(video_cid(id))
    u='https://api.bilibili.com/x/player/playurl?cid='+c+'&bvid='+id+'&qn=64&type=&otype=json'
    aid_json=requests.get(u,headers=header)
    s=aid_json.text
    contents=json.loads(s)
    data=contents['data']['durl'][0]['url']
    data1=contents['data']['durl'][0]['size']
    h=re.findall("http://(.+)com",data)
    flv_host=h[0]+"com"
    head['host']=flv_host
    res = requests.get(data,headers=head,stream=True, verify=False)
    name=video_name(id)
    chunk_size=1024
    with open("{name}.flv".format(name=name), "wb") as f:
        for i in res.iter_content(chunk_size):
            f.write(i)
    print("视频地址：",data+"\n","大小：",data1)

if __name__ == '__main__':
    url = 'https://www.bilibili.com/video/'
    id = argv[1] #input("id:")
    url1 = url + id
    get_flv(id=id)

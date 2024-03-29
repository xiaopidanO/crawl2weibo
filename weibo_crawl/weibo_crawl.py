from urllib.parse import urlencode
from pyquery import PyQuery as pq
import requests
base_url = 'https://m.weibo.cn/api/container/getIndex?'
global id_num
id_num = input("请输入对方的id:",)
global page
page = input("请输入要爬取的页数:")
Referer = "https://m.weibo.cn/u/{}".format(id_num)
headers = {
    'Host': 'm.weibo.cn',
    'Referer': Referer,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

def get_page(page):
    containerid = "107603{}".format(id_num)
    params = {
        'type': 'uid',
        'value': id_num,
        'containerid': containerid,
        'page': page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)

def parse_page(json):
    if json:
        items = json['data']['cards']
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text()
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            yield weibo

if __name__ == '__main__':
    for page in range(1, int(page)):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print(result)

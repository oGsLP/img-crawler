# from selenium import webdriver

# External import

import re
import time
import requests
import json
import os

# Internal import

import util.current as current
from util.change_scale import encode_b64
from weibo.read_preset import read_preset
from util.str_check import is_contain_chinese

# Fixed global variables ------------------

y_n_regex = '([yY](es)?)|([Nn](o|ot)?)'
y_regex = '[yY](es)?'
n_regex = '[Nn](o|ot)?'

weibo_url = "https://m.weibo.cn/"

# -------------------------------------------


# Customizable global variables -------------

pre_id = '230413'
post_id = '230283'

'''
WEIBO_SECOND_PROFILE_WEIBO 全部
WEIBO_SECOND_PROFILE_WEIBO_ORI 原创
WEIBO_SECOND_PROFILE_WEIBO_VIDEO 视频
WEIBO_SECOND_PROFILE_WEIBO_ARTICAL 文章
WEIBO_SECOND_PROFILE_WEIBO_WEIBO_SECOND_PROFILE_WEIBO_PIC 文章
'''
weibo_type = 'WEIBO_SECOND_PROFILE_WEIBO_ORI'

request_params = {"ajwvr": "6", "domain": "100505", "domain_op": "100505", "feed_type": "0", "is_all": "1",
                  "is_tag": "0", "is_search": "0"}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'm.weibo.cn',
    'Pragma': 'no-cache',
    'Referer': "url",
    # User-Agent 根据自己的电脑修改
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'X-Requested-With': 'XMLHttpRequest'
}

# cookie 去网页版获取，具体可以百度
cookie = 'MLOGIN=0; _T_WM=ec3cbb7caac2b6d765aa1c64e065ee7c; OUTFOX_SEARCH_USER_ID_NCOO=200622491.85643607; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D2302832101822767%26from%3Dpage_100306%26fid%3D2304132101822767_-_WEIBO_SECOND_PROFILE_PIC%26uicode%3D10000011'

preset_default_path = "./weibo_uid.txt"
root = "_pics/"

# -------------------------------------------


# Simple global variables -------------------

cur_page = 1
n = 1
page_pics_num = 0
total_pics_num = 0
none_sign = False
page_total = 0
uid = ""
name = ""


# -------------------------------------------


def generate_url(_uid):
    return 'https://m.weibo.cn/api/container/getIndex?containerid=' + pre_id + _uid + '_-_' \
           + weibo_type + '&luicode=10000011&lfid=' + post_id + _uid


def crawl_imgs_of_one_user(_user):
    global uid, name
    uid = _user["uid"]
    name = "" if (_user["name"] is None) else _user["name"]
    _url = generate_url(uid)

    # 总页数
    global page_total, none_sign
    page_total = int(get_total_page(_url))
    none_sign = False

    # 遍历每一页
    for i in range(1, page_total):
        if none_sign:
            print('  (无) 当前页数: ' + str(i) + ', 总页数: ' + str(page_total - 1) + ";")
            time.sleep(0.2)
        else:
            headers['Cookie'] = cookie
            print(_url)
            if i > 1:
                _url = _url + '&page_type=03&page=' + str(i)
            # print(_url)
            response = requests.get(_url, headers=headers)
            # print(response.url)
            html = response.text
            _json = json.loads(html)
            get_cur_page_weibo(_json, i)
            # 休眠1秒
            time.sleep(1)
            if page_total > 10:
                if i % 10 == 0 and not none_sign:
                    # 每爬10页休眠10秒
                    time.sleep(10)
    print()
    print("用户[%s]: %s 爬取完成" % (uid, name))
    print()


# 保存图片到本地
def save_image(img_src, date, pid, i):
    # print(img_src)
    _dir = root + str(name)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    if is_contain_chinese(date):
        date = current.get_date()
    elif date[0:2] == "20":
        date = date[2:]
    else:
        if len(date) == 5:
            date = str(current.get_year()) + "-" + date
    _name = _dir + '/' + str(date) + '_' + str(encode_b64(int(i)))[2:] + '_' + str(pid + 1) + '.jpg'

    if not os.path.exists(_name):
        r = requests.get(img_src)
        r.raise_for_status()

        with open(_name, "wb") as f:
            f.write(r.content)
        print("    %s  爬取完成" % _name)
    else:
        print("    %s  文件已存在" % _name)


# 获取当前页的数据
def get_cur_page_weibo(_json, i):
    global name
    if i == 1:
        if len(name) == 0:
            name = _json['data']['cards'][0]['mblog']['user']['screen_name']
        print("开始爬取 用户[%s]: %s" % (uid, name))

    _cards = _json['data']['cards']
    _cardListInfo = _json['data']['cardlistInfo']
    global cur_page
    # page_total = _cardListInfo['total']  # 你要爬取的微博的页数
    cur_page = i  # 当前微博页数
    global none_sign
    if _cardListInfo['page'] is None:
        none_sign = True

    print('  当前页数: ' + str(cur_page) + ', 总页数: ' + str(page_total - 1) + ";")
    # 打印微博
    for card in _cards:
        if card['card_type'] == 9:
            if card['mblog']['weibo_position'] == 1:
                card['mblog'].setdefault('pics', False)
                if card['mblog']['pics']:
                    for x in range(len(card['mblog']['pics'])):
                        # 保存图片到本地
                        save_image(card['mblog']['pics'][x]['large']['url'], card['mblog']['created_at'], x,
                                   card['mblog']['mid'])
                        time.sleep(1)
                        # print(card['mblog'])


# 获取总页数
def get_total_page(_url):
    _response = requests.get(_url, headers=headers)
    print(_response.url)
    print()
    _html = _response.text
    __json = json.loads(_html)
    return __json['data']['cardlistInfo']['total']  # 你要爬取的微博的页数


def set_root_path():
    global root
    val = input("3)input your object dir path (default current dir): ").strip()
    if len(val) == 0:
        print("  use current directory...")
    elif not os.path.exists(val):
        print("  path '%s' does not exist, will use current directory..." % val)
    else:
        root = val


def crawl():
    use_preset = input('1)use preset or not? y|n: ').strip()
    while not re.match(y_n_regex, use_preset):
        print("  wrong input, try again! ")
        use_preset = input('2)use preset or not? y|n: ').strip()

    if re.match(y_regex, use_preset):
        preset_path = input('  input preset path (default "%s"): ' % preset_default_path).strip()
        path_len = len(preset_path)
        if not (path_len == 0 and os.path.exists(preset_path)):
            print("    preset path exists")
        else:
            preset_path = preset_default_path
            if path_len == 0:
                print('    will use default path: "%s"' %
                      preset_path)
            else:
                print('    preset path does not exist, will use default path: "%s"' %
                      preset_path)
            users = read_preset(preset_path)
            set_root_path()
            for user in users:
                crawl_imgs_of_one_user(user)
                time.sleep(1)
    elif re.match(n_regex, use_preset):
        _uid = input('2)input weibo id: ')
        set_root_path()
        crawl_imgs_of_one_user({"name": None, "uid": _uid})


if __name__ == '__main__':
    crawl()

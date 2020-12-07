# -*- coding: utf-8 -*-

import hashlib
import requests
import urllib3
import urllib
import os

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

def make_sure_dir_exists(dir_name):
    if (not os.path.exists(dir_name)):
        os.makedirs(dir_name)

def download_img_by_title(title):
    print (title)
    api = 'http://tu.ekj.com/images.php?v=1&key=&text='
    api = api + urllib.parse.quote(title)
    #header = {"Authorization": "Bearer " + api_token} # 设置http header，视情况加需要的条目，这里的token是用来鉴权的一种方式
    r = requests.get(api, stream=True)
    print(r.status_code) # 返回状态码
    make_sure_dir_exists('images')
    if r.status_code == 200:
        dest_file_name = 'images\\'+hashlib.md5(title.encode("utf8")).hexdigest()
        dest_file_name = dest_file_name + '.jpg'
        open(dest_file_name, 'wb').write(r.content) # 将内容写入图片
        print("done")
    del r

if __name__ == "__main__":
    #make_sure_dir_exists('xxxxxxxxxxxxx')
    #print(get_ai_article('床前明月光'))
    print('ok')
    download_img_by_title('床前明月光')
    #print(get_rand_title())
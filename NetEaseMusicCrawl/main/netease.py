import pymongo
import requests
import time
from Crypto.Cipher import AES
import base64
import json
import random

# client = pymongo.MongoClient("mongodb+srv://Kevin:kevin7755@cluster0-djvxv.mongodb.net/test?retryWrites=true&w=majority")
# db = client.test
# mongo_collection = db.netease


forth_param = "0CoJUm6Qyw8W8jud"
second_key = 16 * 'F'

headers = {
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

def search_keyword(keyword):

    url = "http://music.163.com/api/search/get/web"

    query = {
        "type": 1,
        "s": keyword,
        "limit": 1,
    }
    try:
        res = requests.get(url, headers=headers, params=query).json()
        result = res['result']['songs'][0]['id']
        song_id = str(result)
        return song_id
    except:
        raise


def aesEncrypt(text, Key):
    pad = 16 - len(text) % 16
    text = text + (pad * chr(pad)).encode('utf-8')
    iv = '0102030405060708'
    encryptor = AES.new(Key.encode('utf-8'), 2, iv.encode('utf-8'))
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


def getRTComments(song_id):
    url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_" + song_id + "/?csrf_token="
    try:
        for i in range(0, 1):
            if i == 0:
                first_param = b"{rid:\"\", offset:\"" + str(i * 20).encode('utf-8') + b"\", total:\"true\", limit:\"20\", csrf_token:\"\"}"
            else:
                first_param = b"{rid:\"\", offset:\"" + str(i * 20).encode('utf-8') + b"\", total:\"false\", limit:\"20\", csrf_token:\"\"}"
            data = {
                "params": aesEncrypt(aesEncrypt(first_param, forth_param), second_key),
                "encSecKey": get_encSecKey()
            }
            res = requests.post(url, headers=headers, data=data).json()
            c_list = []
            for j in range(0, 20):
                data = res['comments'][j]
                c_list.append(data)
            # try:
            #     mongo_collection.insert_many(c_list)
            # except:
            #     raise
            time.sleep(random.randint(3, 6))
            return c_list
    except:
        raise

def getHotComments(song_id):
        url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_" + song_id + "/?csrf_token="
        try:
            for i in range(0, 1):
                if i == 0:
                    first_param = b"{rid:\"\", offset:\"" + str(i * 20).encode(
                        'utf-8') + b"\", total:\"true\", limit:\"20\", csrf_token:\"\"}"
                else:
                    first_param = b"{rid:\"\", offset:\"" + str(i * 20).encode(
                        'utf-8') + b"\", total:\"false\", limit:\"20\", csrf_token:\"\"}"
                data = {
                    "params": aesEncrypt(aesEncrypt(first_param, forth_param), second_key),
                    "encSecKey": get_encSecKey()
                }
                res = requests.post(url, headers=headers, data=data).json()
                c_list = []
                for j in range(0, 15):
                    data = res['hotComments'][j]
                    c_list.append(data)
                print(c_list)
                # try:
                #     mongo_collection.insert_many(c_list)
                # except:
                #     raise
                time.sleep(random.randint(3, 6))
                return c_list
        except:
            raise

getHotComments(search_keyword("我和我的祖国"))

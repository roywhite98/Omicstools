import http.client
import hashlib
import urllib
import random
import json
from pip._vendor.distlib.compat import raw_input

def baidu_translation(content, targetLang='zh'):
    '''
    输入一段文本，转换为别的语言
    '''
    appid = '20210117000673628' #我的appid
    secretKey = 'Iu851rh7KWjDCO871hAT' #我的密钥
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content # 翻译内容，q存放
    fromLang = 'auto' # 原文语种
    toLang = targetLang # 译文语种, 默认为中文
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    # 建立会话，返回结果
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()        #response是HTTPResponse对象
        jsonResponse = response.read().decode("utf-8")  # 获得返回的结果，结果为json格式
        js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构
        dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
        return(dst)  # 打印结果
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
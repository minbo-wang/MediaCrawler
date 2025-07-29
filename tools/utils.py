# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。  


import argparse
import logging

from .crawler_util import *
from .slider_util import *
from .time_util import *


def init_loging_config():
    level = logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(name)s %(levelname)s (%(filename)s:%(lineno)d) - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    _logger = logging.getLogger("MediaCrawler")
    _logger.setLevel(level)
    return _logger


logger = init_loging_config()

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
    

import requests
import json

def send_wechat_link_message(corpid, corpsecret, agentid, user_id, title, description, url, picurl=None):
    # 获取access_token
    token_url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}'
    token_response = requests.get(token_url)
    access_token = token_response.json().get('access_token')
    
    # 构造消息体
    message_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
    message = {
        "touser": user_id,  # 可以是@all发送给所有人
        "msgtype": "news",
        "agentid": agentid,
        "news": {
            "articles": [
                {
                    "title": title,
                    "description": description,
                    "url": url,
                    "picurl": picurl if picurl else ""
                }
            ]
        }
    }
    
    # 发送消息
    response = requests.post(message_url, data=json.dumps(message, ensure_ascii=False).encode('utf-8'))
    return response.json()

def send_url(note_detail):
    # 使用示例
    corpid = "wwcd27e8fbd9ed06ff"
    corpsecret = "uNZeW_SYNJHEvL5iPnYZu7-gXUp7gydlW_7VYXxgUMM"
    agentid = "1000002"
    user_id = "WangMinBo" #"@ALL"

    url = note_detail['url']
    title = note_detail['title']
    description = note_detail['desc']
    picture = note_detail['image_list'][0]['url_default']
    # url = "https://www.xiaohongshu.com/explore/688279dc000000001c037451?xsec_token=AB-02jqtS4XAXqKj_NJVfECXUp2AzvtL_L8oIrcdc1Epg=&xsec_source=None"

    result = send_wechat_link_message(corpid, corpsecret, agentid, user_id, title, description, url, picture)
    print(result)

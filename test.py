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

# 使用示例
corpid = "wwcd27e8fbd9ed06ff"
corpsecret = "uNZeW_SYNJHEvL5iPnYZu7-gXUp7gydlW_7VYXxgUMM"
agentid = "1000002"
user_id = "WangMinBo" #"@ALL"

title = "这是一个HTML链接"
description = "点击查看详细内容"
url = "https://www.xiaohongshu.com/explore/688279dc000000001c037451?xsec_token=AB-02jqtS4XAXqKj_NJVfECXUp2AzvtL_L8oIrcdc1Epg=&xsec_source=None"

result = send_wechat_link_message(corpid, corpsecret, agentid, user_id, title, description, url)
print(result)
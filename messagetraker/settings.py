choose_steam='''Input which message tracker you want to check:
v: 2A VIP;      1: 1A;      2: 1B       3: 1C;
4: 1D;      5: 1E;      6: 1F;      
7: 1G;      8: 3A;      9: 3B'''

steams_dict={
    "v":"2A VIP",
    "1":"1A",
    "2":"1B",
    "3":"1C",
    "4":"1D",
    "5":"1E",
    "6":"1F",
    "7":"1G",
    "8":"3A",
    "9":"3B",
}

message_tracker_dict={
        "v":"https://b2bi2-sword.dc.signintra.com/ui/",
        "1":"https://b2bi1-sword.dc.signintra.com/ui/",
        "2":"https://b2bi3-sword.dc.signintra.com/ui/",
        "3":"https://b2bi4-sword.dc.signintra.com/ui/",
        "4":"https://b2bi5-sword.dc.signintra.com/ui/",
        "5":"https://b2bi6-sword.dc.signintra.com/ui/",
        "6":"https://b2bi7-sword.dc.signintra.com/ui/",
        "7":"https://b2bi8-sword.dc.signintra.com/ui/",
        "8":"https://b2bimcpapp1.sl3.comp.db.de:6443/ui/",
        "9":"https://b2bimcpapp2.sl3.comp.db.de:6443/ui/",
}

user_id="xxx"
password="xxx!"

from_id="xxx"

phonemessage_statusStr = {
    '0': '短信发送成功',
    '-1': '参数不全',
    '-2': '服务器空间不支持,请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
    '30': '密码错误',
    '40': '账号不存在',
    '41': '余额不足',
    '42': '账户已过期',
    '43': 'IP地址限制',
    '50': '内容含有敏感词'
}

phonemessage_smsapi = "xxx"
# 短信平台账号
phonemessage_user = 'xxx'
# 短信平台密码
def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()

phonemessage_password = md5('xxx')
# 要发送的短信内容
# content = char_handle()
# print(content)
# 要发送短信的手机号码
# phonemessage_phone = 'xxx'
phonemessage_phone = 'xxx'

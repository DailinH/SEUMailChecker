import sys
import email
import imaplib
import json
from time import sleep
from threading import Thread


with open("config.json") as config_file:
    config_json = json.load(config_file)
    imap_server = config_json["imap"]["server"]
    imap_user = config_json["imap"]["user"]
    imap_password = config_json["imap"]["password"]
    check_interval = config_json["interval"]


mail_conn = imaplib.IMAP4_SSL(imap_server)
(ret, caps) = mail_conn.login(imap_user, imap_password)


if __name__ == "__main__":
    current_latest_mail_id = 0 # 记录当前的最新邮件的id

    while True:
        mail_conn.list() # 获取邮件箱列表 
        mail_conn.select("inbox") # 选择当前邮件箱为收件箱；btw，不清楚这三步中哪一步才正式向服务器取数据……
        (result, messages) = mail_conn.search(None, "ALL") # 获取收件箱的所有邮件ID

        if result == "OK":
            latest_mail_id = messages[0].split(b" ")[-1] # 获取最新的邮件id
            if current_latest_mail_id != latest_mail_id:
                (ret, res) = mail_conn.fetch(latest_mail_id, "RFC822") # 根据id向服务器发送请求
                msg = email.message_from_bytes(res[0][1]) # 从响应中解析出邮件头（没有正文）
                
                # 进一步验证 or 做要做的事
                print(msg["Subject"]) # 打印邮件标题
                pass

                current_latest_mail_id = latest_mail_id # 更新最新的邮件id

        print("After this round, current latest mail id is", current_latest_mail_id.decode("utf-8"))
        sleep(check_interval) # 等待一小段时间后再次检查
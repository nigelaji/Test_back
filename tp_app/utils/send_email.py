# coding:utf-8
from tp_app import app, mail
from flask import jsonify, request
import traceback
from flask_mail import Message
import threading


@app.route('/send_email')
def send_email():
    ret = {
        'code': 200,
        'msg': '邮件发送成功',
        'data': {}
    }
    if request.method == 'POST':
        try:
            _send_mail('点下面链接验证邮箱', '60s点此链接www.xxx.com账号生效', '838863149@qq.com', 'forsakenlimbo@gmail.com')
        except Exception as e:
            fail_details = traceback.format_exc()
            ret['msg'] = '邮件发送失败：%s' % fail_details
    return jsonify(ret)


def send_async_email(app_, msg):  # 异步发送邮件
    with app_.app_context():
        mail.send(msg)


def _send_mail(subject='测试标题', body='测试正文', sender='838863149@qq.com', recipients=None):
    """Message参数
    subject：邮件主题标题
    recipients：收件人
    body：纯文本消息正文
    html：HTML格式的消息正文
    sender：发件人
    cc：略
    bcc：略
    attachments：附件实例列表
    reply_to：回复
    date：发送日期
    charset：消息字符集
    extra_headers：略
    mail_options：略
    rcpt_options：略
    """
    if recipients is None:
        raise ValueError('收件人必填！')
    msg = Message(subject=subject, body=body)
    msg.sender = sender
    msg.recipients = recipients

    # Flask支持很多，比如附件和抄送等功能，根据需要自己添加就可以
    # msg.attach 邮件附件添加
    # msg.attach("文件名", "类型", 读取文件）
    #     with app.open_resource("F:\2281393651481.jpg") as fp:
    #         msg.attach("image.jpg", "image/jpg", fp.read())
    thr = threading.Thread(target=send_async_email, args=[app, msg])  # 创建线程
    thr.start()


def send_mail(subject='测试标题', body='测试正文', sender='838863149@qq.com', recipients=None):
    """
    在应用上下文之外发送邮件
    """
    if recipients is None:
        raise ValueError('收件人必填！')
    msg = Message(subject=subject, body=body)
    msg.sender = sender
    msg.recipients = recipients

    # Flask支持很多，比如附件和抄送等功能，根据需要自己添加就可以
    # msg.attach 邮件附件添加
    # msg.attach("文件名", "类型", 读取文件）
    #     with app.open_resource("F:\2281393651481.jpg") as fp:
    #         msg.attach("image.jpg", "image/jpg", fp.read())
    thr = threading.Thread(target=mail.send, args=(msg,))  # 创建线程
    thr.start()

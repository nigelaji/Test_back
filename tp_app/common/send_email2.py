# coding:utf-8
import smtplib
from tp_app.config import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_SSL
from tp_app.decos import async_exec


@async_exec
def send_mail(message, sender='838863149@qq.com', recipients=None):
    """
    在应用上下文之外发送邮件
    """
    if recipients is None:
        raise ValueError('收件人必填！')
    smtpObj = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
    smtpObj.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    smtpObj.sendmail(sender, recipients, message)

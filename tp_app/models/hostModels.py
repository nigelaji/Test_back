# coding:utf-8
from tp_app import db
from datetime import datetime

__all__ = [
    'Host', 'HostUser'
]


class Host(db.Model):
    """主机管理表"""
    __tablename__ = 'tp_host_management'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), comment='昵称')
    hostname = db.Column(db.String(64), comment='hostname')
    ip_addr = db.Column(db.String(30), comment='主机IP')
    port = db.Column(db.Integer, comment='连接端口')
    enabled = db.Column(db.Boolean, comment='是否可用')


class HostUser(db.Model):
    """主机用户表，与主机多对多"""
    __tablename__ = 'tp_host_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), comment='账户')
    password = db.Column(db.String(128), comment='密码')

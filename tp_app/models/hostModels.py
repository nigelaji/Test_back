# coding:utf-8
from tp_app import db

__all__ = [
    'Host', 'init_host_data'
]


class Host(db.Model):
    """主机管理表"""
    __tablename__ = 'tp_host_management'
    id = db.Column(db.Integer, primary_key=True)
    ip_addr = db.Column(db.String(30), comment='主机IP')
    port = db.Column(db.Integer, comment='连接端口')
    username = db.Column(db.String(30), comment='主机账号')
    password = db.Column(db.String(30), comment='主机密码')

    def __init__(self, ip_addr, port, username, password):
        self.ip_addr = ip_addr
        self.port = port
        self.username = username
        self.password = password
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Host (ip_addr='%r', port='%r')>" % (self.ip_addr, self.port)

    @staticmethod
    def init_host():  # 初始化管理员用户
        host = Host.query.filter_by().first()
        if not host:
            print('初始化主机表')
            Host(ip_addr='192.168.1.2', port='22', username='root', password='123456')
            Host(ip_addr='192.168.1.3', port='22', username='root', password='123456')


def init_host_data():  # 对表进行数据初始化
    Host.init_host()

# coding:utf-8
import random
import textwrap

from tp_app import db
from datetime import datetime

# class Article(db.Model):
#     """文章管理表"""
#     __tablename__ = 'tp_host_management'
#     id = db.Column(db.Integer, primary_key=True)
#     elasticsearch_id = db.Column(db.String(64), comment='文档数据库唯一索引')

__all__ = [
    'Article', 'Comment', 'article_comment', 'init_article_data'
]

article_comment = db.Table('tp_article_comment',  # 文章评论关联表
                           db.Column('article_id', db.Integer, db.ForeignKey('tp_article.id')),
                           db.Column('comment_id', db.Integer, db.ForeignKey('tp_comment.id'))
                           )


class Article(db.Model):
    """文章管理表"""
    __tablename__ = 'tp_article'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('tp_user.id'))
    title = db.Column(db.String(100), comment="标题")
    content = db.Column(db.Text, comment="内容")
    keywords = db.Column(db.String(100), comment="关键词")
    status = db.Column(db.CHAR(1), default=1, comment='软删除, 0已删除，1正常状态，默认值1')
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, index=True)  # index=True，查询用户列表时，加快速度
    hot = db.Column(db.Integer, comment="热度")
    comments = db.relationship('Comment', secondary=article_comment, backref=db.backref('article', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('article', lazy='dynamic'))

    def __init__(self, user_id, title, content, keywords, status='1'):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.keywords = keywords
        self.status = status
        self.hot = random.randint(10, 100)
        db.session.add(self)
        db.session.commit()

    @property
    def serialize(self):  #
        if self.status == '0':
            return {}
        return {
            'title': self.title,
            'content': self.content,
            'keywords': self.keywords,
            'update_time': self.update_time,
            'hot': self.hot,
            'user': self.user.username
        }

    @staticmethod
    def init_test_data():
        from tp_app.models.authModels import User
        article = Article.query.filter_by(id=1).first()
        if not article:
            print('初始化测试数据文章表')
            user = User.query.filter_by(id=1).first()
            Article(user.id, '文章标题', '文章内容文章内容文章内容文章内容文章内容文章内容文章内容文章内容文章内容文章内容', '测试')

    def __repr__(self):
        return "<Article (id='%r', title='%r')>" % (self.id, textwrap.shorten(self.title, width=20, placeholder="..."))


class Comment(db.Model):
    """文章评论表"""
    __tablename__ = 'tp_comment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('tp_user.id'))
    content = db.Column(db.String(1000), comment="内容")
    level = db.Column(db.CHAR(1), default=1, comment="评论等级，评论文章的全部是1级评论，回复的全部是二级评论")
    parent_comment_id = db.Column(db.Integer, default=0, comment="父级评论id，默认为0")
    parent_comment_userid = db.Column(db.Integer, default=0, comment="父级评论的userid，默认为0")
    reply_comment_id = db.Column(db.Integer, default=0, comment="被回复的评论id，默认为0")
    reply_comment_userid = db.Column(db.Integer, default=0, comment="被回复的评论的userid，默认为0")
    status = db.Column(db.CHAR(1), default=1, comment='软删除, 0已删除，1正常状态，默认值1')
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, index=True)  # index=True，查询用户列表时，加快速度
    hot = db.Column(db.Integer, comment="点赞数")
    top_status = db.Column(db.CHAR(1), default=0, comment='0不置顶，1置顶')

    def __init__(self, user_id, content, status='1', **kwargs):
        self.user_id = user_id
        self.content = content
        self.status = status
        self.hot = random.randint(10, 100)
        for k,v in kwargs:
            setattr(self, k, v)
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def init_test_data():
        from tp_app.models.authModels import User
        comment = Comment.query.filter_by(id=1).first()
        if not comment:
            print('初始化测试数据评论表')
            user1 = User.query.filter_by(id=1).first()
            Comment(user1.id, '评论内容')
            user2 = User.query.filter_by(id=2).first()
            Comment(user2.id, "评论用户的评论")

    def __repr__(self):
        return "<Comment (id='%r', content='%r')>" % (
            self.id, textwrap.shorten(self.content, width=30, placeholder="..."))


def init_article_data():  # 对关联表进行数据初始化
    Article.init_test_data()
    # Comment.init_test_data()

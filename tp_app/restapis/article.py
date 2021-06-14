# coding:utf-8
from flask_restful import Resource, reqparse
from tp_app import db
from tp_app.models.articleModels import Article, Comment
import traceback

ret = {
    'code': 200,
    'data': {},
    'msg': '',

}


class ArticleListAPI(Resource):
    def get(self):
        articles = Article.query.all()
        ret['data'] = [article.serialize for article in articles]
        return ret

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('title', type=str, required=True, help='required', location='json')
        parse.add_argument('content', type=str, required=True, help='required', location='json')
        parse.add_argument('keywords', type=str, location='json')
        parse.add_argument('uid', required=True, help='no uid', location='headers')
        kwargs = parse.parse_args()
        try:
            session_id = kwargs.pop('uid')
            article = Article(user_id=session_id, **kwargs)
            db.session.add(article)
            db.session.commit()
            ret['msg'] = '文章新增成功'
        except Exception:
            ret['code'] = 500
            ret['msg'] = traceback.format_exc()
        return ret


class ArticleAPI(Resource):
    def get(self, id):
        article = Article.query.filter_by(id=id).first()
        if article:
            ret['data'] = article.serialize
        else:
            ret['msg'] = '用户不存在'
        return ret

    def put(self, id):
        parse = reqparse.RequestParser()
        parse.add_argument('title', type=str, required=True, help='required', location='json')
        parse.add_argument('content', type=str, required=True, help='required', location='json')
        parse.add_argument('keywords', type=str, location='json')
        parse.add_argument('uid', required=True, help='no uid', location='headers')
        kwargs = parse.parse_args()
        article = Article.query.filter_by(id=id).first()
        uid = kwargs.pop('uid')
        if article:
            if uid == article.user_id:
                for k, v in kwargs.items():
                    if v is None:
                        break
                    setattr(article, k, v)
                db.session.add(article)
                db.session.commit()
                ret['msg'] = "修改成功"
            else:
                ret['msg'] = '权限不允许'
        else:
            ret['msg'] = '文章不存在'
        return ret

    def delete(self, id):
        article = Article.query.filter_by(id=id).first()
        if article:
            db.session.delete(article)
            db.session.commit()
            ret['msg'] = '删除成功'
        return ret


article_resources = [
    {
        'resource': ArticleListAPI,
        'urls': '/articles'
    },
    {
        'resource': ArticleAPI,
        'urls': '/articles/<int:id>'
    },
]

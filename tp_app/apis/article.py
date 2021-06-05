# coding:utf-8
from flask_restful import Resource, reqparse
from tp_app.models.articleModels import Article


class ArticleListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided', location='json')
        self.reqparse.add_argument('description', type=str, default="", location='json')
        super(ArticleListAPI, self).__init__()

    def get(self):
        return {
            'code': 200
        }

    def post(self):
        pass


class ArticleAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='必填', location='json')
        self.reqparse.add_argument('content', type=str, required=True, help='必填', location='json')
        super(ArticleAPI, self).__init__()

    def get(self, id):
        article = Article.query.filter_by(id=id).first()
        return {
            "title": article.title,
            "content": article.content
        }

    def post(self, ):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


article_resouces = [
    {
        'resource': ArticleAPI,
        'urls': '/v1/article/<int:id>'
    },
    {
        'resource': ArticleListAPI,
        'urls': '/v1/article/list'
    }
]

# coding:utf-8
from flask_restful import Resource, Api
from tp_app.models.articleModels import Article


class ArticleListAPI(Resource):
    def get(self):
        pass

    def post(self):
        pass


class ArticleAPI(Resource):
    def get(self, id):
        article = Article.query.filter_by(id=id).first()
        return {
            "title": article.title,
            "content": article.content
        }

    def put(self, id):
        pass

    def delete(self, id):
        pass


Api.add_resource(ArticleAPI, '/<int:id>')

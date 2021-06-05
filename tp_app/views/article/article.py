# coding:utf-8
from flask_restful import Resource, Api
from tp_app.models.articleModels import Article


class ArticleResource(Resource):
    def get(self, id):
        article = Article.query.filter_by(id=id).first()
        return {
            "title": article.title,
            "content": article.content
        }


Api.add_resource(ArticleResource, '/<int:id>')

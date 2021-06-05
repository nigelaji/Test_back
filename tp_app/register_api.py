from tp_app.apis.article import ArticleListAPI, ArticleAPI


def register_api(api):
    api.add_resource(ArticleAPI, '/v1/article/<int:id>')
    api.add_resource(ArticleListAPI, '/v1/article/list')

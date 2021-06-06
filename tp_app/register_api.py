from tp_app.apis.user import auth_resources
from tp_app.apis.article import article_resources

resources = []
resources.extend(auth_resources)
resources.extend(article_resources)


def register_api(api):
    for resource in resources:
        api.add_resource(resource['resource'], resource['urls'])

    # api.add_resource(ArticleListAPI, '/v1/article/list')

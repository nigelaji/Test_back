from tp_app.restapis.user import auth_resources
from tp_app.restapis.article import article_resources
import inspect
from tp_app.views.auth.auth import require_token
resources = []
resources.extend(auth_resources)
resources.extend(article_resources)


def register_api(api):
    for resource in resources:
        for name, member in inspect.getmembers(resource['resource'], lambda m: inspect.isfunction(m)):
            setattr(resource['resource'], name, require_token(member))
        api.add_resource(resource['resource'], resource['urls'])

    # api.add_resource(ArticleListAPI, '/v1/article/list')

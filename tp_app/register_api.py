from tp_app.apis.user import auth_resources

resources = []
resources.extend(auth_resources)


def register_api(api):
    for resource in resources:
        api.add_resource(resource['resource'], resource['urls'])

    # api.add_resource(ArticleListAPI, '/v1/article/list')

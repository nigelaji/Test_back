# coding:utf-8
from flask import jsonify, request, session, Response, abort, g
from tp_app.views import article_blue
import traceback
from tp_app.models.articleModels import Article




@article_blue.route('/list', methods=['GET'])  # 获取文章内容
def get_article():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    try:
        articles = Article.query.all()
        ret['data'] = []
    except Exception as e:
        traceback.print_exc()
        ret['code'] = -1
        ret['msg'] = "%s" % e
    return jsonify(ret)


@article_blue.route('', methods=['GET'])  # 获取文章内容
def get_article():
    ret = {
        'code': 200,
        'msg': '',
        'data': {}
    }
    try:
        article_id = request.args.get('id')
        article = Article.query.filter_by(id=article_id).first()
        ret['data'] = {
            'title': article.title,
            'content': article.content
        }
    except Exception as e:
        traceback.print_exc()
        ret['code'] = -1
        ret['msg'] = "%s" % e
    return jsonify(ret)



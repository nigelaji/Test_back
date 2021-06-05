from datetime import datetime
from elasticsearch import Elasticsearch

# 创建es实例
es = Elasticsearch(hosts=["localhost:9200"])


# 定义文档，类似于创建一张表，很多地方叫索引
# 定义文章表
# title 文章标题
# content 文章内容
# keyword 关键字
# createTime 创建时间
# updateTime 修改时间
def define_index():
    """
    https://www.elastic.co/guide/cn/elasticsearch/guide/current/index-management.html  查看索引管理帮助文档
    settings
        number_of_shards
            每个索引的主分片数，默认值是 5 。这个配置在索引创建后不能修改。
        number_of_replicas
            每个主分片的副本数，默认值是 1 。对于活动的索引库，这个配置可以随时修改。
    mappings 映射是定义文档及其包含的字段的存储和索引方式的过程。每个文档都是字段的集合，每个字段都有自己的 数据类型。
    """
    article_index = {
        "settings": {},
        "mappings": {
            "properties": {
                "title": {  # 类似于字段
                    "type": "text",
                    "index": True,  # True可以加快搜索
                    # "analyzer": "ik_max_word",  # 这个会对中文标题进行最大限度的拆分，便于搜索关键字。ik_smart这是粗粒度拆分。两种分词器使用的最佳实践是：索引时用ik_max_word，在搜索时用ik_smart。
                    "search_analyzer": "ik_smart"
                    # whitespace 这种是已文档中空格进行分词，一般用于英文，单词与单词之间都是空格
                },
                "content": {
                    "type": "text",
                },
                # "timestamp": {
                #     "type": "long",
                #     "format": "strict_date_optional_time"
                # },
                "label": {
                    "type": "text",
                    "index": True,
                    "analyzer": "whitespace"
                },
                "createTime": {
                    "type": "date",
                },
                "updateTime": {
                    "type": "date",
                }
            }

        }
    }
    es.indices.create(index="article_index", body=article_index)


# 插入数据
def insert_data(index, ):
    # 插入数据
    dt_now = datetime.now()
    es.index(
        index="test", 
        doc_type="_doc",
        id=1,
        body={"title": "标题", "content": "内容", "label": "test", "createTime": dt_now, "updateTime": dt_now}
    )
    # 可以不用指定id，create会自动添加id。
    es.create(index="test", doc_type="_doc", id=2, body={"id": 2, "name": "小红"})

    return


# 查询数据
def search(index, doc_type, **kwargs):
    # 查询数据
    # es.get(index="test", doc_type="_doc", id=1)
    # es.search(index="test", doc_type="_doc", body=query)
    # 滚动分页的func，第四块部分 分页查询中 说明
    # es.scroll(scroll_id="scroll_id", scroll="5m")
    return


def update_index():
    # 修改字段
    es.update(index="test", doc_type="_doc", id=1, body={"doc": {"name": "张三"}})
    return


# 删除数据
def delete_data():
    # 删除指定数据
    es.delete(index='test', doc_type='_doc', id=1)
    return


# 删除文档
def delete_index(index):
    es.indices.delete(index=index)


if __name__ == '__main__':
    define_index()

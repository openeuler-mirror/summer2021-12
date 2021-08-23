from elasticsearch import Elasticsearch, helpers
from flask import Blueprint

bp = Blueprint('es', __name__, cli_group=None)


def sync_es():
    from faq.models import EQuestionDescription
    es = init_es()
    create_index(es)
    q_dps = EQuestionDescription.query.filter()
    dp: EQuestionDescription
    body_l = [{
        "_index": "question",
        "_source": {"description": dp.description,
                    "qid": dp.question_id,
                    "labels": [tagging.tag.tag_name for tagging
                               in dp.question.r_question_taggings]}
    } for dp in q_dps]
    helpers.bulk(client=es, actions=body_l)


def create_index(_es):
    if _es.indices.exists(index='question'):
        _es.delete_by_query(index='question', body={"query": {"match_all": {}}})
    else:
        _es.indices.create(index='question', body={"settings": get_setting(), "mappings": get_question_mappings()})
    if _es.indices.exists(index='answer'):
        _es.delete_by_query(index='answer', body={"query": {"match_all": {}}})
    else:
        _es.indices.create(index='answer', body={"settings": get_setting(), "mappings": get_answer_mappings()})


def get_setting():
    settings = {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 2
        }
    }

    return settings


def get_question_mappings():
    mappings = {
        "properties": {
            "qid": {
                "type": "keyword"
            },
            "labels": {
                "type": "keyword"
            },
            "description": {
                "type": "text"
            }
        }
    }

    return mappings


def get_answer_mappings():
    mappings = {
        "properties": {
            "qid": {
                "type": "keyword"
            },
            "summary": {
                "type": "text"
            },
            "content": {
                "type": "text"
            }
        }
    }

    return mappings


def init_es(secret_file='faq_secret.ini') -> Elasticsearch:
    import configparser

    config = configparser.ConfigParser()
    config.read(secret_file)
    assert 'elastic' in config
    if 'cloud_id' in config['elastic'] \
            and "user" in config['elastic'] \
            and 'password' in config['elastic']:
        _es = Elasticsearch(
            cloud_id=config['elastic']['cloud_id'],
            http_auth=(config['elastic']['user'], config['elastic']['password'])
        )
    else:
        # todo: assert local elasticsearch
        _es = Elasticsearch()
    return _es


if __name__ == "__main__":
    create_index(init_es())

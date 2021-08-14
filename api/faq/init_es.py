from elasticsearch import Elasticsearch
import pprint


def create_index(es):
    q_body = dict()
    q_body['settings'] = get_setting()
    q_body['mappings'] = get_question_mappings()

    a_body = dict()
    a_body['settings'] = get_setting()
    q_body['mappings'] = get_answer_mappings()
    pprint.pprint(q_body) 
    pprint.pprint(a_body)
    es.indices.create(index='questions', body=q_body)
    es.indices.create(index='answers', body=a_body)


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
            "descriptions": {
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


def init_es():
    import configparser

    config = configparser.ConfigParser()
    config.read('faq_secret.ini')

    es = Elasticsearch(
        cloud_id=config['elastic']['cloud_id'],
        http_auth=(config['elastic']['user'], config['elastic']['password'])
    )
    create_index(es)


if __name__ == "__main__":
    init_es()

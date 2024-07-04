# -*- coding: utf-8 -*-
from typing import Optional, List
from ..client.mongo_client import Mongo
from ..model.entity import BatchSpider
from ..model.enums import CommonStatus


def _build_task_group_key(task_group, plat_code):
    return {'_id': f'{task_group}:{plat_code}:group'}


def _build_stream_spider_key(task_type, plat_code):
    return f'{task_type}:{plat_code}'


# 获取爬虫任务组配置
def get_spider_group(task_group, plat_code):
    return Mongo().get('zcbot_spider_group', _build_task_group_key(task_group, plat_code))


# 获取portainer爬虫配置
def get_spider(spider_id: str, status: CommonStatus = CommonStatus.ON) -> Optional[BatchSpider]:
    row = Mongo().get('zcbot_spider', {'spiderId': spider_id, 'status': status.name})
    if not row:
        return None
    return BatchSpider(**row)


# 获取支持网站平台
def get_platforms_by_spider_group(task_type: str):
    return Mongo().aggregate('zcbot_platforms', [
        {
            '$lookup': {
                'from': 'zcbot_spider_group',
                'localField': '_id',
                'foreignField': 'plat_code',
                'as': 'spider'
            }
        },
        {
            '$match': {'spider.task_type': task_type.lower()}
        },
        {
            '$project': {'spider': 0}
        },
        {'$sort': {'sort': 1}}
    ])


def get_spiders_by_id(spider_ids: List):
    _query = {
        "_id": {
            "$in": spider_ids
        },
        "status": "ON"
    }
    rs = Mongo().list("zcbot_spider", query=_query)
    return rs

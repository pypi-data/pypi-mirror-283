import logging
from pymongo import MongoClient
from redis import Redis
from pymongo import UpdateOne
from typing import List
from zcbot_cacke_sdk.constant import ZCBOT_CACHE_MONGO_URL, ZCBOT_CACHE_MONGO_DATABASE, ZCBOT_CACHE_REDIS_URL
from zcbot_cacke_sdk.utils import singleton
from model import CacheSkuPoolModel


@singleton
class CacheSku(object):

    logger = logging.getLogger(__name__)

    def __init__(self, mongo_url: str = None, mongo_database: str = None, redis_url: str = None):
        self.mongo_url = mongo_url or ZCBOT_CACHE_MONGO_URL
        self.mongo_database = mongo_database or ZCBOT_CACHE_MONGO_DATABASE
        self.client = MongoClient(self.mongo_url)
        self.redis_url = redis_url or ZCBOT_CACHE_REDIS_URL
        self.rds_client = Redis.from_url(url=self.redis_url, decode_responses=True)

    """
    判断是否存在
    根据id列表判断商品池是否包含
    """
    def contains(self, ids: List[str]):
        set_name = 'zcbot:cache:sku'
        # 使用pipeline来优化多个SISMEMBER命令的执行
        with self.rds_client.pipeline() as pipe:
            # 创建一个与id列表大小相同的列表，用于存储结果
            results = [None] * len(ids)
            # 构建pipeline中的命令
            for index, _id in enumerate(ids):
                pipe.sismember(set_name, _id)
            # 执行pipeline中的所有命令，并获取结果
            for index, result in enumerate(pipe.execute()):
                results[index] = result

        # 根据结果将存在的ID和不存在的ID分别放入两个列表中
        existing_ids = [_id for index, _id in enumerate(ids) if results[index]]
        non_existing_ids = [_id for index, _id in enumerate(ids) if not results[index]]

        return existing_ids, non_existing_ids

    """
    获取缓存数据
    根据id列表获取缓存数据
    """
    def get(self, ids: List[str]):
        try:
            documents = []  # 初始化一个空列表来存储文档
            client = MongoClient(self.mongo_url)
            rs = client.get_database(self.mongo_database).get_collection('cache_sku_pool').find(
                {'linkSn': {'$in': ids}})
            for document in rs:
                documents.append(document)  # 将每个文档添加到列表中
            return documents
        except Exception as e:
            self.logger.error(e)
        finally:
            try:
                self.client.close()
            except Exception as e:
                self.logger.error(e)

    """
    写入缓存数据
    将商品数据写入缓存（mongo+redis）
    """
    def save(self, skuList: List[CacheSkuPoolModel]):
        try:
            # 验证skuList
            if not skuList:
                raise ValueError("数据不能为空")
            update_bulk = []
            # 准备要插入的文档列表
            valid_skus = [sku for sku in skuList if sku.skuName and sku.brandName]
            link_ids = [sku.linkSn for sku in valid_skus if sku.linkSn]
            # MongoDB插入操作
            for sku in valid_skus:
                update_bulk.append(UpdateOne(
                    filter={'_id': sku.linkSn},
                    update={'$set': sku.dict()},
                    upsert=True
                ))
            if update_bulk:
                collection = self.client.get_database(self.mongo_database).get_collection('cache_sku_pool')
                collection.bulk_write(update_bulk)
            # Redis插入操作
            set_name = 'zcbot:cache:sku'
            self.rds_client.sadd(set_name, *link_ids)
        except Exception as e:
            self.logger.error(e)
        finally:
            try:
                self.client.close()
            except Exception as e:
                self.logger.error(e)
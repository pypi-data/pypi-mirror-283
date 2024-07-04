import asyncio
from typing import TYPE_CHECKING, Type, Union

from scrapy.utils.defer import deferred_from_coro

from gzspidertools.common.multiplexing import ReuseOperation
from gzspidertools.scraper.pipelines.es import dynamic_es_document

try:
    from elasticsearch import AsyncElasticsearch
    from elasticsearch.helpers import async_bulk
except ImportError:
    # pip install gzspidertools[database]
    pass

__all__ = ["AyuAsyncESPipeline"]

if TYPE_CHECKING:
    from elasticsearch_dsl import Document

    from gzspidertools.common.typevars import ESConf, slogT

    DocumentType = Union[Type[Document], type]


class AyuAsyncESPipeline:
    es_conf: "ESConf"
    slog: "slogT"
    client: "AsyncElasticsearch"
    es_type: "DocumentType"
    running_tasks: set

    def open_spider(self, spider):
        assert hasattr(spider, "es_conf"), "未配置 elasticsearch 连接信息！"
        self.running_tasks = set()
        self.es_conf = spider.es_conf
        _hosts_lst = self.es_conf.hosts.split(",")
        if any([self.es_conf.user is not None, self.es_conf.password is not None]):
            http_auth = (self.es_conf.user, self.es_conf.password)
        else:
            http_auth = None
        self.client = AsyncElasticsearch(
            hosts=_hosts_lst,
            basic_auth=http_auth,
            verify_certs=self.es_conf.verify_certs,
            ca_certs=self.es_conf.ca_certs,
            client_cert=self.es_conf.client_cert,
            client_key=self.es_conf.client_key,
            ssl_assert_fingerprint=self.es_conf.ssl_assert_fingerprint,
        )

    async def process_item(self, item, spider):
        item_dict = ReuseOperation.item_to_dict(item)
        alert_item = ReuseOperation.reshape_item(item_dict)
        if not (new_item := alert_item.new_item):
            return

        _index = alert_item.table.name
        if not hasattr(self, "es_type"):
            fields_define = {k: v.notes for k, v in item_dict.items()}
            index_define = self.es_conf.index_class
            index_define["name"] = _index
            self.es_type = dynamic_es_document("ESType", fields_define, index_define)
            if self.es_conf.init:
                self.es_type.init()

        task = asyncio.create_task(self.insert_item(new_item, _index))
        self.running_tasks.add(task)
        await task
        task.add_done_callback(lambda t: self.running_tasks.discard(t))
        return item

    async def insert_item(self, new_item, index):
        async def gendata():
            yield {
                "_index": index,
                "doc": new_item,
            }

        await async_bulk(self.client, gendata())

    async def _close_spider(self):
        await self.client.close()

    def close_spider(self, spider):
        return deferred_from_coro(self._close_spider())

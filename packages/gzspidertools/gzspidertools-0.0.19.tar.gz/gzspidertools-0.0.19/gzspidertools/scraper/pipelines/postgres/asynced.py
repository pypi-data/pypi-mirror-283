from typing import TYPE_CHECKING

from scrapy.utils.defer import deferred_from_coro

from gzspidertools.common.expend import PostgreSQLPipeEnhanceMixin
from gzspidertools.common.multiplexing import ReuseOperation

try:
    from psycopg_pool import AsyncConnectionPool
except ImportError:
    # pip install gzspidertools[database]
    pass

__all__ = [
    "AyuAsyncPostgresPipeline",
]

if TYPE_CHECKING:
    from gzspidertools.common.typevars import PostgreSQLConf, slogT


class AyuAsyncPostgresPipeline(PostgreSQLPipeEnhanceMixin):
    postgres_conf: "PostgreSQLConf"
    slog: "slogT"
    pool: "AsyncConnectionPool"
    running_tasks: set

    def open_spider(self, spider):
        assert hasattr(spider, "postgres_conf"), "未配置 PostgreSQL 连接信息！"
        self.running_tasks = set()
        self.slog = spider.slog
        self.postgres_conf = spider.postgres_conf
        return deferred_from_coro(self._open_spider(spider))

    async def _open_spider(self, spider):
        self.pool = AsyncConnectionPool(
            f"dbname={self.postgres_conf.database} "
            f"user={self.postgres_conf.user} "
            f"host={self.postgres_conf.host} "
            f"port={self.postgres_conf.port} "
            f"password={self.postgres_conf.password}",
            open=False,
        )
        await self.pool.open()

    async def process_item(self, item, spider):
        async with self.pool.connection() as conn:
            item_dict = ReuseOperation.item_to_dict(item)
            alter_item = ReuseOperation.reshape_item(item_dict)
            new_item = alter_item.new_item
            sql = self._get_sql_by_item(table=alter_item.table.name, item=new_item)
            await conn.execute(sql, tuple(new_item.values()))
        return item

    async def _close_spider(self):
        await self.pool.close()

    def close_spider(self, spider):
        return deferred_from_coro(self._close_spider())

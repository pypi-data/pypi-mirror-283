from typing import TYPE_CHECKING

from pymysql import cursors
from twisted.enterprise import adbapi

from gzspidertools.common.expend import MysqlPipeEnhanceMixin
from gzspidertools.common.multiplexing import ReuseOperation
from gzspidertools.common.mysqlerrhandle import TwistedAsynchronous, deal_mysql_err

__all__ = [
    "AyuTwistedMysqlPipeline",
]

if TYPE_CHECKING:
    from gzspidertools.common.typevars import MysqlConf, slogT


class AyuTwistedMysqlPipeline(MysqlPipeEnhanceMixin):
    mysql_conf: "MysqlConf"
    slog: "slogT"
    dbpool: "adbapi.ConnectionPool"

    def open_spider(self, spider):
        assert hasattr(spider, "mysql_conf"), "未配置 Mysql 连接信息！"
        self.slog = spider.slog
        self.mysql_conf = spider.mysql_conf
        # 判断目标数据库是否连接正常。若连接目标数据库错误时，创建缺失的目标数据库。
        self._connect(self.mysql_conf).close()

        _mysql_conf = {
            "user": self.mysql_conf.user,
            "password": self.mysql_conf.password,
            "host": self.mysql_conf.host,
            "port": self.mysql_conf.port,
            "db": self.mysql_conf.database,
            "charset": self.mysql_conf.charset,
            "cursorclass": cursors.DictCursor,
        }
        self.dbpool = adbapi.ConnectionPool("pymysql", cp_reconnect=True, **_mysql_conf)
        query = self.dbpool.runInteraction(self.db_create)
        query.addErrback(self.db_create_err)

    def db_create(self, cursor):
        pass

    def db_create_err(self, failure):
        self.slog.error(f"创建数据表失败: {failure}")

    def process_item(self, item, spider):
        item_dict = ReuseOperation.item_to_dict(item)
        query = self.dbpool.runInteraction(self.db_insert, item_dict)
        query.addErrback(self.handle_error, item)
        return item

    def db_insert(self, cursor, item):
        alter_item = ReuseOperation.reshape_item(item)
        if not (new_item := alter_item.new_item):
            return

        _table_name = alter_item.table.name
        _table_notes = alter_item.table.notes
        note_dic = alter_item.notes_dic
        sql, args = self._get_sql_by_item(
            table=_table_name,
            item=new_item,
            odku_enable=self.mysql_conf.odku_enable,
        )

        try:
            cursor.execute(sql, args)
        except Exception as e:
            self.slog.warning(
                f"Pipe Warn: {e} & Table: {_table_name} & Item: {new_item}"
            )
            deal_mysql_err(
                TwistedAsynchronous(),
                err_msg=str(e),
                cursor=cursor,
                mysql_conf=self.mysql_conf,
                table=_table_name,
                table_notes=_table_notes,
                note_dic=note_dic,
            )
            return self.db_insert(cursor, item)
        return item

    def handle_error(self, failure, item):
        self.slog.error(f"插入数据失败:{failure}, item: {item}")

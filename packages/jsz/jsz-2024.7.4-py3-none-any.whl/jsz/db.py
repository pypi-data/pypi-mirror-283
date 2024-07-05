"""
数据库工具
"""

from .tools import now
from .tools import logger
from .tools import to_excel

__all__ = [
    "connect_to_mongodb",
    "redisdb",
    "mongodb",
    "mongo_distinct",
    "mongo_sample",
    "mongo_tongji",
]

def redisdb(host="localhost", port=6379, db=0, password=None):
    """
    连接 redis 数据库
    """
    import redis

    return redis.Redis(host=host, port=port, db=db, password=password)


def mongodb(host, database, port: int | None = None, **kwargs):
    """
    连接 MongoDB

    host: mongo 链接
    database: 数据库名称
    port: mongo 端口

    host 有密码格式: "mongodb://username:password@192.168.0.1:27017/"
    host 无密码格式: "mongodb://192.168.0.1:27017/"
    """
    from pymongo import MongoClient

    try:
        # 连接到 MongoDB
        client = MongoClient(host, port, **kwargs)
        db = client[database]
        db.list_collection_names()
        logger.success(f"MongoDB 成功连接到 {database}")
        return db
    except Exception as e:
        logger.error("MongoDB 连接失败:", str(e))
        return None


connect_to_mongodb = mongodb


def mongo_sample(
    mongodb,
    table: str,
    match: dict,
    *,
    size: int = 1000,
    excel: bool = True,
) -> list:
    """
    mongodb 随机样本抽样

    mongodb: mongo 库
    table: mongo 表(集合)名称
    match: 匹配条件，默认不筛选
    size: 随机样本数量
    """
    if not match:
        match = {}
    results = list(
        mongodb[table].aggregate(
            [
                {"$match": match},
                {"$sample": {"size": size}},
            ]
        )
    )
    if excel:
        import pandas as pd

        filename = f"{now(7)}_{table}_sample_{size}.xlsx"
        df = pd.DataFrame(results)
        to_excel(df, filename)

    return results


def mongo_tongji(
    mongodb,
    prefix: str = "",
    tongji_table: str = "tongji",
) -> dict:
    """
    统计 mongodb 每个集合的`文档数量`

    mongodb: mongo 库
    prefix: mongo 表(集合)前缀, 默认空字符串可以获取所有表, 字段名称例如 `统计_20240101`。
    tongji_table: 统计表名称，默认为 tongji
    """

    tongji = mongodb[tongji_table]
    key = prefix if prefix else f"统计_{now(7)}"
    collection_count_dict = {
        **(
            tongji.find_one({"key": key}).get("count")
            if tongji.find_one({"key": key})
            else {}
        ),
        **(
            {
                i: mongodb[i].estimated_document_count()
                for i in mongodb.list_collection_names()
                if i.startswith(prefix)
            }
        ),
    }
    tongji.update_one(
        {"key": prefix if prefix else f"统计_{now(7)}"},
        {"$set": {"count": collection_count_dict}},
        upsert=True,
    )
    return dict(sorted(collection_count_dict.items()))


def mongo_distinct(table, *fields):
    """
    mongo distinct 去重

    table: mongo 表(集合)
    fields: 字段名称，支持多个字段
    """
    pipeline = [{"$group": {"_id": {i: f"${i}" for i in fields}}}]
    agg_results = table.aggregate(pipeline)
    results = [i["_id"] for i in agg_results]
    return results

def mongo_to_csv(table, filename):
    """
    mongo 导出 csv

    table: mongo 表(集合)
    filename: 导出的 csv 文件名
    """
    import csv

    with open(filename, "w", newline="") as csvfile:
        fieldnames = table.find_one().keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for doc in table.find():
            writer.writerow(doc)
            

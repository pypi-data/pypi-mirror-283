from time import time

from bson import ObjectId
from sqlalchemy import text, create_engine
from typing_extensions import List, Optional, Dict, Callable

from neems_to_sql.logger import CustomLogger, logging
from neems_to_sql.neems_to_sql import mongo_collection_to_list_of_dicts, parse_arguments, \
    get_mongo_uri, connect_to_mongo_and_get_client, filter_neems


def execute_query_in_mongo(mongo_db, mongo_neem_ids: List,
                           mongo_query_name: str,
                           query_per_neem: Callable[[ObjectId], List[Dict]],
                           coll_to_use_in_aggregate: str,
                           limit: Optional[int] = None,
                           number_of_repeats: Optional[int] = 10):
    single_query_time = []
    first_neem_id = mongo_neem_ids[0]
    coll = mongo_db.get_collection(f"{first_neem_id}_{coll_to_use_in_aggregate}")
    query = query_per_neem(first_neem_id)
    number_of_query_lines_per_neem = len(query)
    query.extend([
        {
            "$unionWith": {
                "coll": f"{neem_id}_{coll_to_use_in_aggregate}",
                "pipeline": query_per_neem(neem_id)
            }
        } for neem_id in mongo_neem_ids[1:]
    ])
    if limit is not None:
        query.append({"$limit": limit})
    all_docs = []
    for i in range(number_of_repeats):
        start = time()
        cursor = coll.aggregate(query)
        all_docs = [doc for doc in cursor]
        single_query_time.append(time() - start)
    LOGGER.info(f"Mongo Query: {mongo_query_name}")
    LOGGER.info(f"Avg time for {number_of_repeats} repeats: {sum(single_query_time) / number_of_repeats}")
    LOGGER.info(f"Total number of documents: {len(all_docs)}")
    LOGGER.info(f"Number of query lines per neem: {number_of_query_lines_per_neem}")
    LOGGER.info(f"Number of neems: {len(mongo_neem_ids)}")
    LOGGER.info(f"Number of query lines: {number_of_query_lines_per_neem * len(mongo_neem_ids)}")
    LOGGER.info(f"First doc: {all_docs[0]}")


def execute_query_in_sql(sql_engine, query: str, sql_query_name: str, limit: Optional[int] = None,
                         number_of_repeats: Optional[int] = 10):
    single_query_time = []
    if limit is not None:
        query += f" LIMIT {limit}"
    with sql_engine.connect() as connection:
        for i in range(number_of_repeats):
            start = time()
            result = connection.execute(text(query))
            all_docs = [row for row in result]
            single_query_time.append(time() - start)
    LOGGER.info(f"SQL Query: {sql_query_name}")
    LOGGER.info(f"Avg time for {number_of_repeats} repeats: {sum(single_query_time) / number_of_repeats}")
    LOGGER.info(f"Total number of documents: {len(all_docs)}")
    LOGGER.info(f"First Row: {all_docs[0]}")


def execute_query_in_sql_by_looping_over_neems(sql_engine, query: Callable[[str], str], sql_query_name: str,
                                               neem_ids: List,
                                               number_of_repeats: Optional[int] = 10):
    single_query_time = []
    with sql_engine.connect() as connection:
        for i in range(number_of_repeats):
            start = time()
            all_docs = []
            for neem_id in neem_ids:
                result = connection.execute(text(query(str(neem_id))))
                all_docs.extend([row for row in result])
            single_query_time.append(time() - start)
    LOGGER.info(f"SQL Query: {sql_query_name}")
    LOGGER.info(f"Avg time for {number_of_repeats} repeats: {sum(single_query_time) / number_of_repeats}")
    LOGGER.info(f"Total number of documents: {len(all_docs)}")
    LOGGER.info(f"First Row: {all_docs[0]}")


def get_mongo_task_query_for_neem(neem_id):
    return [{"$match": {"p": "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#executesTask"}},
            {
                "$lookup":
                    {
                        "from": f"{neem_id}_triples",
                        "localField": "o",
                        "foreignField": "s",
                        "as": f"{neem_id}"
                    }
            },
            {"$match": {f'{neem_id}.p': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
                        f'{neem_id}.o': 'http://www.ease-crc.org/ont/SOMA.owl#Gripping'}},
            {
                "$project": {
                    f"{neem_id}.s": 1,
                    f"{neem_id}.p": 1,
                    f"{neem_id}.o": 1
                }
            }]


def get_mongo_pr2_links_query(neem_id):
    # tf_coll = db.get_collection(f"{neem_id}_tf")
    # tf_coll.aggregate([
    #     {"$match": {status: "active"}},
    #     {"$merge": {"into": f"filtered_{neem_id}_tf"}},
    # ])
    return [{"$match": {'s': {"$regex": r"^http://knowrob.org/kb/PR2.owl#", "$options": "i"},
                        'p': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
                        'o': 'http://knowrob.org/kb/urdf.owl#Link'
                        }
             },
            {
                "$project": {'s': {"$substrCP": ['$s', 30,
                                                 {"$subtract": [{"$strLenCP": '$s'}, 1]}]},
                             'p': 1,
                             'o': 1
                             }
            },
            {
                "$lookup":
                    {
                        "from": f"{neem_id}_tf",
                        "localField": "s",
                        "foreignField": "child_frame_id",
                        "as": f"{neem_id}_pr2_links_tf"
                    }
            },
            {"$project": {f"{neem_id}_pr2_links_tf": 1}},
            {"$unwind": f"${neem_id}_pr2_links_tf"},
            ]


def get_sql_task_query() -> str:
    query = text("""
        SELECT task_type.*
        FROM dul_executesTask AS tasks
        INNER JOIN rdf_type AS task_type ON task_type.s = tasks.dul_Task_o
                                        AND task_type.o = 'soma:Gripping'
        WHERE task_type.neem_id = tasks.neem_id
        """)
    return query.__str__()


def get_sql_pr2_links_query() -> str:
    query = text("""Select tf.*
                    From rdf_type as rdft
                            INNER JOIN tf ON tf.child_frame_id = substring_index(rdft.s, ':', -1)
                                         AND rdft.neem_id = tf.neem_id
                    Where rdft.o = 'urdf:link'
                      AND rdft.s REGEXP '^pr2:'
                      """)
    return query.__str__()


def get_sql_pr2_links_query_per_neem(neem_id: str) -> str:
    # query = text(f"""Select tf.*
    #                  From tf
    #                             INNER JOIN (Select distinct rdft.s, rdft.ID, rdft.neem_id
    #                                         From rdf_type as rdft
    #                                         Where o = 'urdf:link'
    #                                         AND s REGEXP '^pr2:'
    #                                         AND neem_id = \"{neem_id}\") as rdft
    #                                        ON tf.child_frame_id = substring_index(rdft.s, ':', -1)
    #                  Where tf.neem_id = \"{neem_id}\"
    #                     """)
    query = text(f"""Select tf.*
                     From (Select distinct rdft.s, rdft.neem_id
                                          From rdf_type as rdft
                                          Where o = 'urdf:link'
                                            AND s REGEXP '^pr2:'
                                            AND neem_id = \"{neem_id}\") AS rdft
                     INNER JOIN tf ON tf.child_frame_id IN (substring_index(rdft.s, ':', -1))
                     WHERE tf.neem_id = \"{neem_id}\"
                      """)
    return query.__str__()


def filter_neems_and_get_neem_ids(mongo_db, filters: Optional[Dict] = None) -> List[ObjectId]:
    meta = mongo_db.meta
    meta_lod = mongo_collection_to_list_of_dicts(meta)
    if filters is not None:
        meta_lod = filter_neems(meta_lod, filters)
    if len(meta_lod) == 0:
        LOGGER.error("NO NEEMS FOUND (Probably no meta data collection OR no neems with the given filters)")
        raise ValueError("NO NEEMS FOUND (Probably no meta data collection OR no neems with the given filters)")
    mongo_neem_ids = [doc['_id'] for doc in meta_lod]
    LOGGER.debug(f"NEEM IDS: {mongo_neem_ids}")
    return mongo_neem_ids


def connect_to_mongo_and_get_neems_database(input_args):
    if args.mongo_uri is not None:
        MONGODB_URI = input_args.mongo_uri
    else:
        MONGODB_URI = get_mongo_uri(input_args.mongo_username, input_args.mongo_password, input_args.mongo_host,
                                    input_args.mongo_port, input_args.mongo_database)
    mongo_client = connect_to_mongo_and_get_client(MONGODB_URI)
    mongo_db = mongo_client.neems
    return mongo_db


if __name__ == "__main__":
    LOGGER = CustomLogger("MONGO_VS_SQL_QUERY",
                          "mongo_vs_sql_query.txt",
                          logging.DEBUG, reset_handlers=True).get_logger()

    # Parse the arguments and get the mongo and sql uris.
    args = parse_arguments()

    # Initialize the MongoDB client and get the neems database from it.
    db = connect_to_mongo_and_get_neems_database(args)
    neem_ids = filter_neems_and_get_neem_ids(db, {'visibility': True})

    # Initialize the SQL engine.
    engine = create_engine(args.sql_uri)

    # Execute the queries in MongoDB and SQL.
    query_name = "Find all tasks that are of type Gripping."
    execute_query_in_mongo(db, neem_ids, query_name, get_mongo_task_query_for_neem, "triples")
    LOGGER.info("============================================================")
    execute_query_in_sql(engine, get_sql_task_query(), query_name)

    LOGGER.info("##################################################################################")
    query_name = "Find all pr2 links."
    execute_query_in_mongo(db, neem_ids, query_name, get_mongo_pr2_links_query, "triples",
                           number_of_repeats=1)
    # execute_query_in_sql(engine, get_sql_pr2_links_query(), query_name, limit=1000)
    execute_query_in_sql_by_looping_over_neems(engine, get_sql_pr2_links_query_per_neem, query_name, neem_ids,
                                               number_of_repeats=1)
    LOGGER.info("##################################################################################")

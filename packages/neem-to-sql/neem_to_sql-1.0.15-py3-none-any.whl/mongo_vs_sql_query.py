from time import time

from bson import ObjectId
from neem_query import NeemQuery, RdfType, Tf, TaskType, TfHeader
from sqlalchemy import text, create_engine
from typing_extensions import List, Optional, Dict, Callable

from neems_to_sql.logger import CustomLogger, logging
from neems_to_sql.neems_to_sql import mongo_collection_to_list_of_dicts, parse_arguments, \
    get_mongo_uri, connect_to_mongo_and_get_client, filter_neems


def execute_query_in_mongo(mongo_db, mongo_neem_ids: List,
                           mongo_query_name: str,
                           coll_to_use_in_aggregate: str,
                           query: List[Dict],
                           limit: Optional[int] = None,
                           number_of_repeats: Optional[int] = 10):
    single_query_time = []
    first_neem_id = mongo_neem_ids[0]
    if coll_to_use_in_aggregate in ["triples", "tf"]:
        coll_name = lambda neem_id: f"{neem_id}_{coll_to_use_in_aggregate}"
    else:
        coll_name = lambda _: coll_to_use_in_aggregate
    coll = mongo_db.get_collection(coll_name(first_neem_id))
    number_of_query_lines_per_neem = len(query)
    if limit is not None:
        query.append({"$limit": limit})
    # json_formatted_str = json.dumps(query, indent=2)
    # LOGGER.info(f"QUERY: {json_formatted_str}")
    all_docs = []
    for i in range(number_of_repeats):
        start = time()
        cursor = coll.aggregate(query)
        all_docs = [doc for doc in cursor]
        single_query_time.append(time() - start)
    avg_time = sum(single_query_time) / number_of_repeats
    LOGGER.info(f"Mongo Query: {mongo_query_name}")
    LOGGER.info(f"Avg time for {number_of_repeats} repeats: {avg_time}")
    LOGGER.info(f"Avg time per doc: {avg_time / len(all_docs)}")
    LOGGER.info(f"Total number of documents: {len(all_docs)}")
    LOGGER.info(f"Number of query lines per neem: {number_of_query_lines_per_neem}")
    LOGGER.info(f"Number of neems: {len(mongo_neem_ids)}")
    LOGGER.info(f"Number of query lines: {number_of_query_lines_per_neem * len(mongo_neem_ids)}")
    LOGGER.info(f"First doc: {all_docs[0]}")


def union_the_mongo_query_on_all_neems(mongo_neem_ids: List, query_per_neem: Callable[[ObjectId], List[Dict]],
                                       coll_to_use_in_aggregate: str, start_query: Optional[List[Dict]] = None,
                                       group_by: Optional[str] = None,
                                       merge_into: Optional[str] = None) -> List[Dict]:
    first_neem_id = mongo_neem_ids[0]
    if start_query is None:
        query = query_per_neem(first_neem_id)
    else:
        query = start_query
        query.extend(query_per_neem(first_neem_id))
    if coll_to_use_in_aggregate in ["triples", "tf"]:
        coll = lambda neem_id: f"{neem_id}_{coll_to_use_in_aggregate}"
    else:
        coll = lambda _: coll_to_use_in_aggregate
    query.extend([
        {
            "$unionWith": {
                "coll": coll(neem_id),
                "pipeline": query_per_neem(neem_id)
            }
        } for neem_id in mongo_neem_ids[1:]
    ])

    if group_by is not None:
        query.append({"$group": {f"_id": f"${group_by}"}})
        query.append({"$project": {f"{group_by}": "$_id"}})

    if merge_into is not None:
        query.append({"$merge": {"into": merge_into}})

    return query


def execute_query_in_sql(sql_engine, query: str, sql_query_name: str, limit: Optional[int] = None,
                         number_of_repeats: Optional[int] = 10):
    single_query_time = []
    if limit is not None:
        query += f" LIMIT {limit}"
    for i in range(number_of_repeats):
        with sql_engine.connect() as connection:
            start = time()
            result = connection.execute(text(query))
            single_query_time.append(time() - start)
            all_docs = [row for row in result]
    log_sql_query_stats(sql_query_name, single_query_time, all_docs, number_of_repeats)


def execute_query_in_sql_using_orm(neem_query: NeemQuery, orm_query_func: Callable[[NeemQuery], NeemQuery], sql_query_name: str,
                                   limit: Optional[int] = None,
                                   number_of_repeats: Optional[int] = 10):
    single_query_time = []
    df = None
    for i in range(number_of_repeats):
        neem_query.reset()
        start = time()
        neem_query = orm_query_func(neem_query)
        if limit is not None:
            neem_query.limit(limit)
        df = neem_query.get_result().df
        single_query_time.append(time() - start)
    log_sql_query_stats(sql_query_name, single_query_time, df.to_numpy().tolist(), number_of_repeats,
                        orm=True)


def get_orm_query_for_tf_data_of_pr2_links(neem_query: NeemQuery):
    pr2_links = (neem_query.select(RdfType.s).filter_by_type(RdfType, ["urdf:link"])
                 .filter(RdfType.s.like("%pr2%")).distinct()).get_result().df["rdf_type_s"].str.split(':').str[-1]
    neem_query.reset()
    return neem_query.select(Tf.child_frame_id, Tf.neem_id).filter(Tf.child_frame_id.in_(pr2_links))


def execute_query_in_sql_by_looping_over_neems(sql_engine, query: Callable[[str], str], sql_query_name: str,
                                               mongo_neem_ids: List,
                                               number_of_repeats: Optional[int] = 10):
    single_query_time = []
    with sql_engine.connect() as connection:
        for i in range(number_of_repeats):
            start = time()
            all_docs = []
            for neem_id in mongo_neem_ids:
                result = connection.execute(text(query(str(neem_id))))
                all_docs.extend([row for row in result])
            single_query_time.append(time() - start)
    log_sql_query_stats(sql_query_name, single_query_time, all_docs, number_of_repeats)


def log_sql_query_stats(sql_query_name: str, single_query_time: List, all_docs: List, number_of_repeats: int,
                        orm: Optional[bool] = False):
    """
    Log the stats of the SQL query.
    Args:
        sql_query_name: The name of the SQL query.
        single_query_time: The time taken for each query.
        all_docs: The list of all the documents (rows) returned by the query.
        number_of_repeats: The number of repeats of the query for time calculation.
        orm: Whether the query is an ORM query or not.
    Returns: None
    """
    avg_time = sum(single_query_time) / number_of_repeats
    if orm:
        LOGGER.info(f"ORM Query: {sql_query_name}")
    else:
        LOGGER.info(f"SQL Query: {sql_query_name}")
    LOGGER.info(f"Avg time for {number_of_repeats} repeats: {avg_time}")
    LOGGER.info(f"Avg time per row: {avg_time / len(all_docs)}")
    LOGGER.info(f"Total number of rows: {len(all_docs)}")
    LOGGER.info(f"First Row: {all_docs[0]}")


def get_mongo_task_query_for_all_neems(mongo_neem_ids: List):
    return union_the_mongo_query_on_all_neems(mongo_neem_ids, get_mongo_task_query_for_neem, "triples")


def get_mongo_task_query_for_neem(neem_id) -> List[Dict]:
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


def get_mongo_query_for_tf_data_of_base_link_for_all_neems(mongo_neem_ids: List):
    query = union_the_mongo_query_on_all_neems(mongo_neem_ids,
                                               lambda x: get_mongo_query_for_tf_data_of_base_link_for_neem(),
                                               "tf")
    return query


def get_mongo_query_for_tf_data_of_base_link_for_neem():
    return [{"$match": {"child_frame_id": "base_link"}}]


def get_mongo_query_for_tf_data_of_pr2_links_for_all_neems(mongo_db, mongo_neem_ids: List):
    query = union_the_mongo_query_on_all_neems(mongo_neem_ids, lambda x: get_mongo_query_for_pr2_links(),
                                               "triples", group_by="pr2_link", merge_into="unique_pr2_links")
    coll = mongo_db.get_collection(f"{mongo_neem_ids[0]}_triples")
    coll.aggregate(query)
    query = union_the_mongo_query_on_all_neems(mongo_neem_ids, join_mongo_tf_on_pr2_links_for_neem,
                                               "unique_pr2_links")
    return query


def get_mongo_query_for_pr2_links():
    return [{"$match": {'s': {"$regex": r"^http://knowrob.org/kb/PR2.owl#", "$options": "i"},
                        'p': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
                        'o': 'http://knowrob.org/kb/urdf.owl#Link'
                        }
             },
            {
                "$project": {'pr2_link': {"$substrCP": ['$s', 30,
                                                        {"$subtract": [{"$strLenCP": '$s'}, 1]}]}
                             }
            }
            ]


def join_mongo_tf_on_pr2_links_for_neem(neem_id):
    return [
        {
            "$lookup":
                {
                    "from": f"{neem_id}_tf",
                    "localField": "pr2_link",
                    "foreignField": "child_frame_id",
                    "as": f"pr2_links_tf"
                }
        },
        {
            "$match": {  # Filters out documents where there is no match
                f"pr2_links_tf.child_frame_id": {"$exists": True}
            }
        },
        {"$project": {f"pr2_links_tf.child_frame_id": 1, "_id": 0}},
        {"$unwind": f"$pr2_links_tf"},
    ]


def get_sql_query_for_task_data() -> str:
    query = text("""
        SELECT task_type.*
        FROM dul_executesTask AS tasks
        INNER JOIN rdf_type AS task_type ON task_type.s = tasks.dul_Task_o
                                        AND task_type.o = 'soma:Gripping'
        WHERE task_type.neem_id = tasks.neem_id
        """)
    return query.__str__()


def get_orm_query_for_task_data(nq: NeemQuery):
    return nq.select_from(TaskType).filter_by_type(TaskType, ["soma:Gripping"])


def get_orm_query_for_tf_data_of_base_link(nq: NeemQuery):
    return nq.select(Tf.child_frame_id, Tf.neem_id).filter(Tf.child_frame_id == "base_link")


def get_sql_query_for_tf_data_of_base_link() -> str:
    query = text("""Select tf.*
                    From tf
                    Where tf.child_frame_id = 'base_link'
                      """)
    return query.__str__()


def get_sql_query_for_tf_data_of_pr2_links() -> str:
    # query = text("""Select tf.*
    #                 From rdf_type as rdft
    #                         INNER JOIN tf ON tf.child_frame_id = substring_index(rdft.s, ':', -1)
    #                                      AND rdft.neem_id = tf.neem_id
    #                 Where rdft.o = 'urdf:link'
    #                   AND rdft.s REGEXP '^pr2:'
    #                   """)
    # query = text(f"""Select tf.*
    #                      From (Select distinct substring_index(rdft.s, ':', -1) as s
    #                                           From rdf_type as rdft
    #                                           Where o = 'urdf:link'
    #                                             AND s REGEXP '^pr2:') AS unique_links
    #                      INNER JOIN tf ON tf.child_frame_id = unique_links.s
    #                       """)
    query = text("""WITH pr2_links AS (
                        SELECT DISTINCT SUBSTRING(rdf_type.s, 5) AS pr2_link_names
                        FROM rdf_type
                        WHERE rdf_type.o = 'urdf:link' AND rdf_type.s like '%pr2%')
                    SELECT pr2_links.*
                    FROM pr2_links
                    INNER JOIN tf ON tf.child_frame_id in (pr2_links.pr2_link_names)
                    """)
    return query.__str__()


def get_sql_query_for_tf_data_of_pr2_links_per_neem(neem_id: str) -> str:
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
                     From (Select distinct substring_index(rdft.s, ':', -1) as s
                                          From rdf_type as rdft
                                          Where o = 'urdf:link'
                                            AND s REGEXP '^pr2:'
                                            AND neem_id = \"{neem_id}\") AS unique_links
                     INNER JOIN tf ON tf.child_frame_id IN (unique_links.s)
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
    nq = NeemQuery(engine=engine)

    # Execute the queries in MongoDB and SQL.
    query_name = "Find all tasks that are of type Gripping."
    execute_query_in_mongo(db, neem_ids, query_name, "triples",
                           get_mongo_task_query_for_all_neems(neem_ids))
    LOGGER.info("============================================================")
    execute_query_in_sql(engine, get_sql_query_for_task_data(), query_name)
    LOGGER.info("============================================================")
    execute_query_in_sql_using_orm(nq, get_orm_query_for_task_data, query_name)

    LOGGER.info("##################################################################################")
    query_name = "Find TF Data for all pr2 links."
    execute_query_in_mongo(db, neem_ids, query_name, "unique_pr2_links",
                           get_mongo_query_for_tf_data_of_pr2_links_for_all_neems(db, neem_ids),
                           number_of_repeats=10)
    LOGGER.info("============================================================")
    execute_query_in_sql(engine, get_sql_query_for_tf_data_of_pr2_links(), query_name, number_of_repeats=10)
    # execute_query_in_sql_by_looping_over_neems(engine, get_sql_pr2_links_query_per_neem, query_name, neem_ids,
    #                                            number_of_repeats=1)
    LOGGER.info("============================================================")
    execute_query_in_sql_using_orm(nq, get_orm_query_for_tf_data_of_pr2_links, query_name, number_of_repeats=10)
    LOGGER.info("##################################################################################")
    query_name = "Find TF Data for base_link,"
    execute_query_in_mongo(db, neem_ids, query_name, "tf",
                           get_mongo_query_for_tf_data_of_base_link_for_all_neems(neem_ids),
                           number_of_repeats=10)
    LOGGER.info("============================================================")
    execute_query_in_sql(engine, get_sql_query_for_tf_data_of_base_link(), query_name, number_of_repeats=10)
    LOGGER.info("============================================================")
    execute_query_in_sql_using_orm(nq, get_orm_query_for_tf_data_of_base_link, query_name, number_of_repeats=10)
    LOGGER.info("##################################################################################")

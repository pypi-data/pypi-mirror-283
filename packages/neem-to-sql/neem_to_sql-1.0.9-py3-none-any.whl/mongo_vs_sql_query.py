from time import time

from bson import ObjectId
from typing_extensions import List, Optional, Dict

from neems_to_sql.logger import CustomLogger, logging
from neems_to_sql.neems_to_sql import mongo_collection_to_list_of_dicts, parse_arguments, \
    get_mongo_uri, connect_to_mongo_and_get_client, filter_neems


def apply_query_on_all_neems(db, neem_ids: List, query_name: str, number_of_repeats: int = 10):
    single_query_time = []
    first_neem_id = neem_ids[0]
    triples = db.get_collection(f"{first_neem_id}_triples")
    query = get_task_query_for_neem(first_neem_id)
    number_of_query_lines_per_neem = len(query)
    query.extend([
        {
            "$unionWith": {
                "coll": f"{neem_id}_triples",
                "pipeline": get_task_query_for_neem(neem_id)
            }
        } for neem_id in neem_ids
    ])
    all_docs = []
    for i in range(number_of_repeats):
        start = time()
        cursor = triples.aggregate(query)
        all_docs = [doc for doc in cursor]
        single_query_time.append(time() - start)
    LOGGER.info(f"Query: {query_name}")
    LOGGER.info(f"ALL DOCS: {all_docs}")
    LOGGER.info(f"Avg time for {number_of_repeats} repeats: {sum(single_query_time)/number_of_repeats}")
    LOGGER.info(f"Total number of documents: {len(all_docs)}")
    LOGGER.info(f"Number of query lines per neem: {number_of_query_lines_per_neem}")
    LOGGER.info(f"Number of neems: {len(neem_ids)}")
    LOGGER.info(f"Number of query lines: {number_of_query_lines_per_neem * len(neem_ids)}")


def get_task_query_for_neem(neem_id):
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


def filter_neems_and_get_neem_ids(db, filters: Optional[Dict] = None) -> List[ObjectId]:
    meta = db.meta
    meta_lod = mongo_collection_to_list_of_dicts(meta)
    if filters is not None:
        meta_lod = filter_neems(meta_lod, filters)
    if len(meta_lod) == 0:
        LOGGER.error("NO NEEMS FOUND (Probably no meta data collection OR no neems with the given filters)")
        raise ValueError("NO NEEMS FOUND (Probably no meta data collection OR no neems with the given filters)")
    neem_ids = [doc['_id'] for doc in meta_lod]
    LOGGER.debug(f"NEEM IDS: {neem_ids}")
    return neem_ids


def connect_to_mongo_and_get_neems_database(args):
    if args.mongo_uri is not None:
        MONGODB_URI = args.mongo_uri
    else:
        MONGODB_URI = get_mongo_uri(args.mongo_username, args.mongo_password, args.mongo_host,
                                    args.mongo_port, args.mongo_database)
    mongo_client = connect_to_mongo_and_get_client(MONGODB_URI)
    db = mongo_client.neems
    return db


if __name__ == "__main__":

    LOGGER = CustomLogger("MONGO_VS_SQL_QUERY",
                          "mongo_vs_sql_query.txt",
                          logging.DEBUG, reset_handlers=True).get_logger()

    # Replace the uri string with your MongoDB deployment's connection string.
    args = parse_arguments()
    db = connect_to_mongo_and_get_neems_database(args)
    neem_ids = filter_neems_and_get_neem_ids(db, {'visibility': True})
    query_name = "Find all tasks that are of type Gripping."
    apply_query_on_all_neems(db, neem_ids, query_name)




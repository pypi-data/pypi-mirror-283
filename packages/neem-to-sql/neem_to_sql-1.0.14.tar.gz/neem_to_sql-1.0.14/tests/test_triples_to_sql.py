import os
from unittest import TestCase

from pymongo import MongoClient
from rdflib import RDFS
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from typing_extensions import Optional

from neems_to_sql import TriplesToSQL, SQLCreator, read_and_convert_neem_meta_data_to_sql, drop_all_tables, \
    create_database_if_not_exists_and_use_it, dict_to_sql, get_value_from_sql


class TestNeemsToSql(TestCase):
    t2sql: TriplesToSQL
    mongo_db: MongoClient
    path: str
    sql_creator: SQLCreator
    read_engine: Engine
    write_engine: Engine
    neem_id: str

    @classmethod
    def setUpClass(cls):
        # Create TriplesToSQL object
        cls.t2sql = TriplesToSQL()

        # Replace the uri string with your MongoDB deployment's connection string.
        MONGODB_URI = "mongodb://localhost:27017/"
        # set a 5-second connection timeout
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000, unicode_decode_error_handler='ignore')
        cls.mongo_db = client.neems
        cls.path = os.path.join(os.path.dirname(__file__), '../neems')
        read_sql_uri = "mysql+pymysql://newuser:password@localhost/test"
        write_sql_uri = "mysql+pymysql://newuser:password@localhost/"
        cls.read_engine = create_engine(read_sql_uri, future=True)
        cls.write_engine = create_engine(write_sql_uri, future=True)
        create_database_if_not_exists_and_use_it(cls.write_engine, 'tests')
        cls.write_engine = create_engine(write_sql_uri + 'tests', future=True)
        drop_all_tables(cls.write_engine)
        cls.sql_creator = SQLCreator(cls.read_engine, tosql_func=cls.t2sql.get_sql_type)
        cls.neem_id = '5fd0f191f3fc822d8e73d715'

    @classmethod
    def tearDownClass(cls):
        # Delete the database
        # delete_database_if_exists(cls.write_engine, 'tests')
        cls.read_engine.dispose()
        cls.write_engine.dispose()

    def tearDown(self):
        drop_all_tables(self.write_engine)
        self.t2sql.reset_graph()
        self.sql_creator.reset_data()

    def test_create_graph_from_mongo(self):
        # Create a graph from the mongo database
        self.create_graph_from_mongo()
        result = self.t2sql.g.query("SELECT * WHERE {\"soma\" ?p " + f"\"{self.t2sql.ns_str['soma']}\"" + "}")
        self.assertTrue(len(result) > 0)
        for row in result:
            self.assertTrue(row.p == RDFS.isDefinedBy)

    def test_convert_graph_to_dict(self):
        # Create a graph from the mongo database and convert it to a dictionary
        self.create_graph_from_mongo()
        predicate_dict = self.t2sql.graph_to_dict(save_path=self.path)
        self.assertTrue(len(predicate_dict) > 0)
        self.assertTrue(os.path.exists(os.path.join(self.path, 'predicate_dict.json')))
        os.remove(os.path.join(self.path, 'predicate_dict.json'))
        self.assertTrue({'s': 'soma', 'o': self.t2sql.ns_str['soma']} in predicate_dict['rdfs_isDefinedBy'])
        self.assertTrue({'s': 'dul:Action_IKMZVXGQ', 'o': 'dul:Action'} in predicate_dict['rdf_type'])

    def test_convert_dict_to_sql(self):
        self.sql_creator.engine = self.write_engine
        meta_lod = read_and_convert_neem_meta_data_to_sql(self.mongo_db,
                                                          self.sql_creator
                                                          , neem_filters={'_id': self.neem_id}
                                                          # , neem_filters={'visibility': True}
                                                          , batch_size=4
                                                          , number_of_batches=0
                                                          )
        print(meta_lod)
        for i in range(len(meta_lod)):
            neem_id = meta_lod[i]['_id']
            self.create_graph_from_mongo(neem_id)
            predicate_dict = self.t2sql.graph_to_dict()
            dict_to_sql(predicate_dict, self.sql_creator, neem_id=neem_id)
        # self.sql_creator.reset_data()
        self.sql_creator.upload_data_to_sql(drop_tables=True)
        col_vals = get_value_from_sql('rdfs_isDefinedBy',
                                      self.write_engine, col_name='o'
                                      , col_value_pairs={'s': 'soma'})
        self.assertTrue(len(col_vals) > 0)
        self.assertTrue(self.t2sql.ns_str['soma'] in col_vals)
        self.assertTrue(col_vals.count(self.t2sql.ns_str['soma']) == 1)

    def create_graph_from_mongo(self, neem_id: Optional[str] = None):
        id_ = neem_id if neem_id is not None else self.neem_id
        triples_collection = self.mongo_db.get_collection(str(id_) + '_triples')
        self.t2sql.mongo_triples_to_graph(triples_collection)

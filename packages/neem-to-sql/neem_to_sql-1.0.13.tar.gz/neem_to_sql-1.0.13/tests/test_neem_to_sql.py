from unittest import TestCase, skip

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import registry, Session
from typing_extensions import Optional

from neems_to_sql import get_sql_uri, connect_to_mongo_and_get_client, \
    get_mongo_neems_and_put_into_sql_database, delete_neems_from_sql_database, set_logging_level, drop_all_tables, \
    create_database_if_not_exists_and_use_it

from pymongo import MongoClient


class NeemToSqlTestCase(TestCase):
    mongo_uri: Optional[str] = "mongodb://localhost:27017/neems"
    mongo_client: MongoClient
    engine: Engine
    session: Session

    @classmethod
    def setUpClass(cls):
        """
        Make sure you have a local mongodb server running on port 27017,
        and a local mysql server running on port 3306, with a database called 'test'
        and a user called 'newuser' with password 'password'.
        it can be done with the following commands:
            >> CREATE USER IF NOT EXISTS 'newuser'@'localhost' IDENTIFIED BY 'password';
            >> GRANT ALL PRIVILEGES ON *.* TO 'newuser'@localhost IDENTIFIED BY 'password';
            >> FLUSH PRIVILEGES;
            >> DROP DATABASE IF EXISTS test;
            >> CREATE DATABASE IF NOT EXISTS test;
        """
        cls.mongo_client = connect_to_mongo_and_get_client(cls.mongo_uri)
        sql_uri = get_sql_uri("newuser", "password", "localhost")
        cls.engine = create_engine(sql_uri, future=True)
        create_database_if_not_exists_and_use_it(cls.engine, 'tests')
        drop_all_tables(cls.engine)
        cls.engine = create_engine(sql_uri + 'tests', future=True)
        cls.session = Session(cls.engine)
        registry().metadata.create_all(cls.engine)
        set_logging_level("DEBUG")

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.close()

    def setUp(self):
        pass

    def tearDown(self):
        self.mongo_client = connect_to_mongo_and_get_client(self.mongo_uri)
        drop_all_tables(self.engine)


class TestNeemToSql(NeemToSqlTestCase):
    def test_sequential_neem_to_sql(self):
        get_mongo_neems_and_put_into_sql_database(self.engine, self.mongo_client,
                                                  number_of_batches=1,
                                                  batch_size=1,
                                                  start_batch=0)
        self.mongo_client = connect_to_mongo_and_get_client("mongodb://localhost:27017/neems")
        get_mongo_neems_and_put_into_sql_database(self.engine, self.mongo_client,
                                                  number_of_batches=1, batch_size=1,
                                                  start_batch=1)

    def test_one_batch(self):
        get_mongo_neems_and_put_into_sql_database(self.engine, self.mongo_client,
                                                  number_of_batches=1, batch_size=4,
                                                  start_batch=3,
                                                  neem_filters={'visibility': True},
                                                  drop_neems=False)

    def test_one_batch_drop(self):
        get_mongo_neems_and_put_into_sql_database(self.engine, self.mongo_client,
                                                  number_of_batches=1, batch_size=4,
                                                  start_batch=3,
                                                  neem_filters={'visibility': True},
                                                  drop_neems=True)

    def test_with_drop(self):
        get_mongo_neems_and_put_into_sql_database(self.engine, self.mongo_client,
                                                  neem_filters={'visibility': True}
                                                  , drop_neems=True,
                                                  number_of_batches=1,
                                                  batch_size=1,
                                                  start_batch=0)
        self.mongo_client = connect_to_mongo_and_get_client("mongodb://localhost:27017/neems")
        get_mongo_neems_and_put_into_sql_database(self.engine, self.mongo_client,
                                                  neem_filters={'visibility': True}
                                                  , number_of_batches=1,
                                                  batch_size=1,
                                                  start_batch=1)

    @skip("This test is too slow")
    def test_2_batches(self):
        get_mongo_neems_and_put_into_sql_database(self.engine, self.mongo_client,
                                                  number_of_batches=2, batch_size=1,
                                                  start_batch=0,
                                                  neem_filters={'visibility': True},
                                                  drop_neems=False)

    # @skip("This test is too slow")
    def test_all_batches(self):
        neem_filters = {'visibility': True}
        get_mongo_neems_and_put_into_sql_database(self.engine, self.mongo_client,
                                                  drop_neems=False,
                                                  neem_filters=neem_filters,
                                                  skip_bad_triples=True,
                                                  allow_increasing_sz=True
                                                  )

    def test_drop_neem(self):
        get_mongo_neems_and_put_into_sql_database(self.engine, self.mongo_client,
                                                  number_of_batches=1, batch_size=4,
                                                  start_batch=3,
                                                  neem_filters={'visibility': True},
                                                  drop_neems=True)
        delete_neems_from_sql_database(self.engine, neem_ids=['641064a2ba2ba183b56ca0de'])
        # assert the neem is deleted
        cmd = text("SELECT * FROM neems WHERE _id = '641064a2ba2ba183b56ca0de';")
        with self.engine.connect() as conn:
            result = conn.execute(cmd)
            self.assertIsNone(result.fetchone())

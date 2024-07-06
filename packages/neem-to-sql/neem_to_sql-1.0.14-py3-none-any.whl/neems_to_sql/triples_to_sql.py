import json
import logging
import os
import re
from copy import deepcopy
from datetime import datetime
from typing import Optional, Tuple, Union, List, Dict

from bson.decimal128 import Decimal128
from pymongo import MongoClient
from pymongo.collection import Collection
from rdflib import Graph, URIRef, RDF, RDFS, OWL, Literal, Namespace, XSD
from rdflib.graph import _PredicateType
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy import text

xsd2py = {XSD.integer: int, XSD.float: float, XSD.double: float, XSD.boolean: bool, XSD.dateTime: datetime,
          XSD.positiveInteger: int, XSD.date: datetime, XSD.time: datetime, XSD.string: str,
          XSD.anyURI: str, XSD.decimal: Decimal128, XSD.nonNegativeInteger: int, XSD.long: int}
py2xsd = {int: XSD.integer, float: XSD.double, bool: XSD.boolean, datetime: XSD.dateTime, str: XSD.string,
          Decimal128: XSD.decimal}
xsd2sql = {XSD.integer: 'INT', XSD.float: 'DOUBLE', XSD.double: 'DOUBLE', XSD.boolean: 'BOOL',
           XSD.positiveInteger: 'INT UNSIGNED', XSD.dateTime: 'DATETIME', XSD.date: 'DATE', XSD.time: 'TIME',
           XSD.string: 'TEXT', XSD.anyURI: 'VARCHAR(255)'}


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_byte_size(value: object) -> Optional[int]:
    """Returns the byte size of the given value .

    Args:
        value (object): [The value to get the byte size of.]

    Raises:
        ValueError: [if the type of the value is unknown.]

    Returns:
        Optional[int]: [The byte size of the value.]
    """
    if isinstance(value, str):
        return len(value.encode('utf-8'))
    elif isinstance(value, (int, bool)):
        return (value.bit_length() + 7) // 8
    elif isinstance(value, float):
        return 8
    elif isinstance(value, datetime):
        return 8
    elif value is None:
        return None
    else:
        raise ValueError(f'Unknown type {type(value)}')


def get_sql_type_from_pyval(val: object, signed: Optional[bool] = True) -> Tuple[str, int]:
    """Returns the sql type and the byte size of the given value.
    
    Args:
        val (object): [The value to get the sql type of.]
        signed (Optional[bool], optional): [If the value is signed. Defaults to True.]
    
    Raises:
        ValueError: [if the type of the value is unknown.]

    Returns:
        Tuple[str, int]: [the sql type and the byte size of the value.]
    """
    pytype = type(val)
    byte_size = get_byte_size(val)
    if pytype == int:
        if byte_size <= 4:
            sqltype = 'INT' if signed else 'INT UNSIGNED'
            byte_size = 4
        elif byte_size <= 8:
            sqltype = 'BIGINT' if signed else 'BIGINT UNSIGNED'
            byte_size = 8
        else:
            sqltype = 'TEXT'
            byte_size = 2 ** 16 - 1
    elif pytype == str:
        if byte_size <= 255:
            sqltype = 'VARCHAR(255)'
            byte_size = 255
        elif byte_size <= 2 ** 16 - 1:
            sqltype = 'TEXT'
            byte_size = 2 ** 16 - 1
        elif byte_size <= 2 ** 24 - 1:
            sqltype = 'MEDIUMTEXT'
            byte_size = 2 ** 24 - 1
        else:  # <= 2**32-1
            sqltype = 'LONGTEXT'
            byte_size = 2 ** 32 - 1
    elif pytype in py2xsd:
        sqltype = xsd2sql[py2xsd[pytype]]
    elif val is None:
        return 'TEXT', 2 ** 16 - 1
    else:
        raise ValueError('Unknown type')
    return sqltype, byte_size


class TriplesToSQL:
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        """Initializes the TriplesToSQL class.
        This class is used to deal with triples data in different formats, and convert it to and from SQL.

        Args:
            logger (Optional[logging.Logger], optional): [The logger to use. Defaults to None.]
        
        Examples:
            >>> from neems_to_sql.triples_to_sql import TriplesToSQL
            >>> t2s = TriplesToSQL()
            >>> import sqlalchemy
            >>> engine = create_engine('mysql+pymysql://username:password@localhost/test?charset=utf8mb4')
            >>> sql_triples_query_string = "SELECT s, p, o FROM test.triples"
            >>> t2s.sql_to_graph(engine, sql_triples_query_string) # This is an RDFLib Graph, which can be used to query the data.
            # If you want the graph as a dictionary, use t2s.graph_to_dict()
            >>> triples_dict = t2s.graph_to_dict() # the outermost keys are the predicates, and the inner keys are subjects and objects,
             and the values are lists, a list for subject and a list for object for each predicate.
        """
        self.data_types = {'types': [], 'values': []}
        self.all_property_types = {}
        self.predicate_dict = {}
        self.type_name = {}
        self.domain = {'s': [], 'o': []}
        self.range = {'s': [], 'o': []}
        self.type = {'s': [], 'o': []}
        soma = Namespace("http://www.ease-crc.org/ont/SOMA.owl#")
        dul = Namespace("http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#")
        iolite = Namespace("http://www.ontologydesignpatterns.org/ont/dul/IOLite.owl#")
        urdf = Namespace("http://knowrob.org/kb/urdf.owl#")
        srdl2_cap = Namespace("http://knowrob.org/kb/srdl2-cap.owl#")
        srdl2_comp = Namespace("http://knowrob.org/kb/srdl2-comp.owl#")
        iai_kitchen = Namespace("http://knowrob.org/kb/IAI-kitchen.owl#")
        pr2 = Namespace("http://knowrob.org/kb/PR2.owl#")
        iai_kitchen_knowledge = Namespace("http://knowrob.org/kb/iai-kitchen-knowledge.owl#")
        knowrob = Namespace("http://knowrob.org/kb/knowrob.owl#")
        iai_kitchen_objects = Namespace("http://knowrob.org/kb/iai-kitchen-objects.owl#")
        dcmi = Namespace("http://purl.org/dc/elements/1.1#")
        known_ns = [OWL, RDF, RDFS, XSD, soma, dul, iolite, urdf, srdl2_cap, iai_kitchen, pr2,
                    iai_kitchen_knowledge, knowrob, iai_kitchen_objects, srdl2_comp, dcmi]
        known_ns_names = ['owl', 'rdf', 'rdfs', 'xsd', 'soma', 'dul', 'iolite', 'urdf', 'srdl2_cap', 'iai_kitchen', 'pr2',
                          'iai_kitchen_knowledge', 'knowrob', 'iai_kitchen_objects', 'srdl2_comp', 'dcmi']
        self.ns = {knsname: kns for knsname, kns in zip(known_ns_names, known_ns)}
        self.ns_str = {knsname: str(kns) for knsname, kns in zip(known_ns_names, known_ns)}
        self.reset_graph()
        self.property_sql_type = {}
        self.logger = logger

    def reset_graph(self) -> None:
        """reset the graph by creating a new one and binding the namespaces.
        """
        self.g = Graph(bind_namespaces="rdflib")
        for knsname, kns in self.ns.items():
            self.g.bind(knsname, kns)
            self.g.add((Literal(knsname.replace('"', '\"')), RDFS.isDefinedBy, Literal(self.ns_str[knsname])))

    def get_sql_type(self, val: object, property_name: Optional[str] = None) -> Tuple[str, int]:
        """Get the SQL type of a value, if this value is an output of a triple property, then the property name should be provided,
        to get the correct SQL type.
        
        Args:
            val (object): The value to get the SQL type of.
            property_name (Optional[str], optional): The property name of the value. Defaults to None.
        
        Returns:
            Tuple[str, int]: The SQL type and the byte size of the value.
        """
        if property_name is not None:
            if property_name in self.property_sql_type:
                return self.property_sql_type[property_name]['type'], self.property_sql_type[property_name]['byte_size']
        sqltype, byte_size = get_sql_type_from_pyval(val)
        return sqltype, byte_size

    def ont_2_py(self, obj: object, name: Union[str, URIRef, "_PredicateType"]) -> object:
        """Convert an object from an ontology to a python object, using the ontology's data types,
        found by the RDFS.range property for the given property name, also it keeps track of the data types used,
        and the values of each data type since the initialisation of the class in the self.property_sql_type dictionary.
        
        Args:
            obj (object): The object to convert.
            name (Union[str, URIRef, "_PredicateType"]): The property name of the object.

        Returns:
            object: The converted object.
        """
        o = obj
        property_name = URIRef(str(name))
        p_n3 = property_name.n3(self.g.namespace_manager)
        p_n3 = re.sub(':|-', '_', p_n3)
        # print(property_name.n3(self.g.namespace_manager))
        for _, _, value in self.g.triples((property_name, RDFS.range, None)):
            val = value.n3(self.g.namespace_manager) if isinstance(value, URIRef) else value
            if val not in self.data_types['types']:
                self.data_types['types'].append(val)
                self.data_types['values'].append(o)
            if property_name not in self.all_property_types:
                self.all_property_types[property_name] = value
            if str(XSD) in str(value) and isinstance(value, URIRef):
                if isinstance(o, Literal):
                    o = xsd2py[value](o.toPython())
                o = Literal(o, datatype=value, normalize=True)
                v = o.value
                key = p_n3 + '.o'
                if key not in self.property_sql_type:
                    self.property_sql_type[key] = {}
                if type(v) in [int, str]:
                    signed = value != XSD.positiveInteger
                    self.property_sql_type[key]['type'], self.property_sql_type[key]['byte_size'] = \
                        get_sql_type_from_pyval(v, signed=signed)
                else:
                    self.property_sql_type[key]['type'] = xsd2sql[value]
                    self.property_sql_type[key]['byte_size'] = get_byte_size(v)
            elif value == self.ns['soma'].array_double:
                str_v = str(o).strip('[]')
                sep = ' ' if ' ' in str_v else ','
                v = list(map(float, str_v.split(sep)))
            else:
                v = str(o)
            return v
        return o

    def sql_to_graph(self, sqlalchemy_engine: Engine, triples_query_string: Optional[str] = None,
                     verbose: Optional[bool] = False) -> None:
        """Convert the SQL triples to a graph.
        
        Args:
            sqlalchemy_engine (Engine): The sqlalchemy engine to connect to the SQL database.
            triples_query_string (Optional[str], optional): The SQL query string to get the triples. Defaults to None.
            verbose (Optional[bool], optional): If True, print the graph as a json, and print the namespaces. Defaults to False.
        """
        triples_query_string = \
            """
            SELECT s, p, o, neem_id
            FROM test.triples
            ORDER BY _id;
            """ \
                if triples_query_string is None else triples_query_string

        # get a connection
        engine = sqlalchemy_engine
        conn = engine.connect()
        curr = conn.execute(text(triples_query_string))

        for v in curr:
            new_v = []
            for i in range(3):
                if 'http' in v[i] and '#' in v[i]:
                    ns_name = v[i].split('#')[0].split('/')[-1].split('.owl')[0]
                    ns_iri = v[i].split('#')[0] + '#'
                    if ns_iri not in self.ns.values():
                        self.ns[ns_name] = Namespace(v[i].split('#')[0] + '#')
                new_v.append(URIRef(v[i].strip('<>')) if '#' in v[i] else Literal(v[i].strip('<>')))
            self.g.add(tuple(new_v))
        conn.commit()
        conn.close()
        if verbose:
            print(json.dumps(self.ns, indent=4))
            print(len(self.ns))

    def mongo_triples_to_graph(self, collection: Union[List[Dict], Collection], verbose: Optional[bool] = False,
                               skip: Optional[bool] = False) -> None:
        """Convert MongoDB triples to RDF graph .

        Args:
            collection (Collection): [A mongo collection of documents]
            verbose (bool, optional): [If True, print the graph as a json, and print the namespaces.]. Defaults to False.
            skip (bool, optional): [If True, skip data with value error of missing columns]. Defaults to False.
        Raises:
            ValueError: [If the triple is missing the object/value key]
        """
        self.reset_graph()
        py2xsd = {int: XSD.integer, float: XSD.float, str: XSD.string, bool: XSD.boolean,
                  list: self.ns['soma'].array_double,
                  datetime: XSD.dateTime}
        if not isinstance(collection, list):
            cursor = collection.find({})
        else:
            cursor = collection
        for docs in cursor:
            assert isinstance(docs, dict)
            if 'o' not in docs and 'v' in docs:
                v = [docs['s'], docs['p'], docs['v']]
            elif 'o' in docs and 'v' not in docs:
                v = [docs['s'], docs['p'], docs['o']]
            else:
                if skip:
                    if self.logger is not None:
                        self.logger.warning(
                            f"Missing Object Column in triple keys {list(docs.keys())}, doc_id: {docs['_id']},"
                            f" the row is skipped.")
                    continue
                else:
                    raise ValueError(f'Missing Object value in triple {docs}')
            new_v = []
            for i in range(3):
                if not isinstance(v[i], str):
                    if isinstance(v[i], Decimal128):
                        v[i] = float(v[i].to_decimal())
                    v_i_type = type(v[i])
                    assert v_i_type in py2xsd, f'Unknown type {v_i_type}'
                    new_v.append(Literal(v[i], datatype=py2xsd[v_i_type]))
                    continue
                v_i = str(v[i])
                # make sure that the predicate uri is correctly formatted
                if i == 1:
                    if 'http' in v_i:
                        if '#' not in v_i:
                            splitted_vi = v_i.split('/')
                            last_vi = splitted_vi[-1]
                            v_i = '/'.join(splitted_vi[:-1]) + '#' + last_vi
                # make sure that the ontology is in the graph, if not add it
                if v_i.startswith('http') and '#' in v_i:
                    ns_name = v_i.split('#')[0].split('/')[-1].split('.owl')[0]
                    ns_iri = v_i.split('#')[0] + '#'
                    v_i_name = v_i.split('#')[1]
                    if '/' in v_i_name:
                        v_i_name = v_i_name.replace('/', '_')
                    if '_:' in v_i_name:
                        v_i_name = v_i_name.replace('_:', '')
                    v_i = ns_iri + v_i_name

                    if ns_iri not in self.ns_str.values():
                        self.ns[ns_name] = Namespace(v_i.split('#')[0] + '#')
                        self.ns_str[ns_name] = v_i.split('#')[0] + '#'
                        self.g.bind(ns_name, self.ns[ns_name])
                        self.g.add((Literal(ns_name), RDFS.isDefinedBy, Literal(self.ns_str[ns_name])))
                v_i = v_i.strip('<>')
                # assert that the predicate name is correctly formatted, because it is used as a sql table name
                if i == 1:
                    if 'http' in v_i:
                        assert v_i.startswith('http') and '#' in v_i, 'Property name must be a URI, not {}'.format(v_i)
                    else:
                        assert '/' not in v_i, 'Property name is not formatted correctly {}'.format(v_i)
                new_v.append(
                    URIRef(v_i.strip('<>')) if '#' in v_i and v_i.startswith('http') else Literal(v_i.strip('<>')))
            self.g.add(tuple(new_v))
        if verbose:
            print(json.dumps(self.ns, indent=4))
            print(len(self.ns))

    def graph_to_dict(self, save_path: Optional[str] = None, graph: Optional[Graph] = None,
                      file_name: Optional[str] = 'predicate_dict.json') -> Dict:
        """Convert the graph to a dictionary of predicates and their subjects and objects.
        
        Args:
            save_path (Optional[str], optional): If not None, save the dictionary as a json file to the specified path.
            Defaults to None.
            graph (Optional[Graph], optional): The graph to convert to a dictionary. Defaults to None.
            file_name (Optional[str], optional): The name of the file to save the dictionary to.
             Defaults to 'predicate_dict.json'.

        Returns:
            Dict: A dictionary of predicates and their subjects and objects.
        """
        predicate_dict = {}
        g = self.g if graph is None else graph
        for s, p, o in g:
            p_n3 = p.n3(g.namespace_manager) if isinstance(p, URIRef) or isinstance(p, Literal) else p
            if p_n3 not in predicate_dict:
                predicate_dict[p_n3] = {'s': [], 'o': []}
            s_n3 = s.n3(g.namespace_manager).strip('<>').strip('"') if isinstance(s, URIRef) or isinstance(s, Literal) else str(s)
            if "iai-kitchen.owl" in s_n3:
                s_n3 = s_n3.replace("iai-kitchen.owl", "IAI-kitchen.owl")
            if '#' in s_n3 and s_n3.startswith('http'):
                s_n3 = URIRef(s_n3).n3(g.namespace_manager)
            s_n3 = s_n3.strip('<>').strip('"')
            predicate_dict[p_n3]['s'].append(s_n3)
            new_o = self.ont_2_py(o, p)

            if type(new_o) == Literal:
                new_o = new_o.toPython()

            if type(new_o) == str:
                if "iai-kitchen.owl" in new_o:
                    new_o = new_o.replace("iai-kitchen.owl", "IAI-kitchen.owl")

                if '#' in new_o and new_o.startswith('http'):
                    new_o = URIRef(new_o).n3(g.namespace_manager)
                new_o = new_o.strip('<>').strip('"')

            if type(new_o) in [URIRef, Literal]:
                new_o = new_o.n3(g.namespace_manager)
                new_o = new_o.strip('<>').strip('"')
            predicate_dict[p_n3]['o'].append(new_o)

        predicate_dict_cp = deepcopy(predicate_dict)
        if 'rdfs:domain' in predicate_dict_cp:
            self.domain['s'].extend(predicate_dict_cp['rdfs:domain']['s'])
            self.domain['o'].extend(predicate_dict_cp['rdfs:domain']['o'])
            self.range['s'].extend(predicate_dict_cp['rdfs:range']['s'])
            self.range['o'].extend(predicate_dict_cp['rdfs:range']['o'])
            self.type['s'].extend(predicate_dict_cp['rdf:type']['s'])
            self.type['o'].extend(predicate_dict_cp['rdf:type']['o'])
        new_predicate_dict = {}
        for p in predicate_dict_cp:
            d, r = 's', 'o'
            dtype = ''
            if p in self.domain['s']:
                d = self.domain['o'][self.domain['s'].index(p)]
                self.type_name[d] = {}
                d = re.sub(':|-', '_', d)
                d += '_s'
                self.type_name[d] = d
                predicate_dict[p][d] = predicate_dict[p]['s']
                del predicate_dict[p]['s']
            if p in self.range['s']:
                r = self.range['o'][self.range['s'].index(p)]
                if r in self.type['s']:
                    idx = self.type['s'].index(r)
                    dtype = self.type['o'][idx]
                if dtype != 'rdfs:Datatype' and 'xsd' not in r:
                    self.type_name[r] = {}
                    r = re.sub(':|-', '_', r)
                    r += '_o'
                    self.type_name[r] = r
                    predicate_dict[p][r] = predicate_dict[p]['o']
                    del predicate_dict[p]['o']
            new_p = re.sub(':|-', '_', p)
            if new_p != p:
                predicate_dict[new_p] = predicate_dict[p]
                del predicate_dict[p]

            keys = list(predicate_dict[new_p].keys())
            k1, k2 = keys[0], keys[1]
            new_predicate_dict[new_p] = [{k1: predicate_dict[new_p][k1][i], k2: predicate_dict[new_p][k2][i]} for i in
                                         range(len(predicate_dict[new_p][k1]))]
        self.predicate_dict.update(predicate_dict)
        if save_path is not None:
            path = os.path.join(save_path, file_name)
            with open(path, 'w') as f:
                json.dump(new_predicate_dict, f, indent=4)
        return new_predicate_dict

    def find_link_in_graph_dict(self, value: str, data: Dict) -> Tuple[Optional[int], Optional[object]]:
        """Find the index of the value in the graph dictionary and return the index and the object.
        
        Args:
            value (str): The value to find.
            data (Dict): The graph dictionary.

        Returns:
            Tuple[Optional[int], Optional[object]]: The index and the object, or None if not found.
        """
        try:
            idx = data['rdf_type']['s'].index(value)
            return idx + 1, data['rdf_type']['o'][idx]
        except:
            return None, None

    def triples_json_filter_func(self, doc: Dict) -> Tuple[Optional[str], Dict, str]:
        """Filter function for the json file to filter out the triples.
        
        Args:
            doc (Dict): The document to filter.

        Returns:
            Tuple[Optional[str], Dict, str]: The name of the object, the document and the iri.
        """
        iri = doc['@id']
        if '@type' in doc.keys():
            name = [dtype.split('#')[1] for dtype in doc['@type']]
            name = [re.sub("(_:)", "", n) for n in name]
            for n in name:
                if 'NamedIndividual' in n:
                    for n2 in name:
                        if 'NamedIndividual' not in n2 \
                                and 'Description' not in n2 \
                                and 'List' not in n2:
                            return n2, doc, iri
        return None, doc, iri


if __name__ == "__main__":
    from .neems_to_sql import json_to_sql, dict_to_sql, SQLCreator
    from tqdm import tqdm

    # Create TriplesToSQL object
    t2sql = TriplesToSQL()

    # Create a graph from the sql database or from the json file
    create_graph_from_sql = False
    create_graph_from_json = False
    create_graph_from_mongo = True

    # Save the graph to a json file
    save_graph_to_json = True

    # Create a sql database from the graph dictionary or from the json file
    create_sql_from_graph_dict = False
    create_sql_from_graph_json = True

    # Create sqlalchemy engine
    sql_url = os.environ['LOCAL_SQL_URL3']
    engine = create_engine(sql_url)

    if create_graph_from_sql:
        # Create a graph from the sql database
        t2sql.sql_to_graph(engine)
    elif create_graph_from_json:
        # Create a graph from the json file
        t2sql.g.parse("test.json", format="json-ld")
    elif create_graph_from_mongo:
        # Create a graph from the mongo database
        # Replace the uri string with your MongoDB deployment's connection string.
        MONGODB_URI = "mongodb://localhost:27017/"
        # set a 5-second connection timeout
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000, unicode_decode_error_handler='ignore')
        db = client.neems
        id = '5fd0f191f3fc822d8e73d715'
        triples_collection = db.get_collection(id + '_triples')
        t2sql.mongo_triples_to_graph(triples_collection)

    if save_graph_to_json:
        # Create a json file from the graph
        t2sql.g.serialize(format='json-ld', encoding='utf-8', destination="test.json")

    if create_sql_from_graph_dict:
        # Create a dictionary from the graph
        predicate_dict = t2sql.graph_to_dict(dump=True)
        sql_creator = SQLCreator(engine)
        dict_to_sql(predicate_dict, sql_creator)
        # print(json.dumps(list(zip(data_types['types'],data_types['values'])),sort_keys=True, indent=4))
        # print(json.dumps(all_property_types,sort_keys=True, indent=4))
        # print("number of datatybes = ", len(data_types['types']))

    elif create_sql_from_graph_json:
        # Create a sql database from the json file
        triples_data = json.load(open('../../test.json'))
        name = "restructred_triples"
        total = json_to_sql(name, triples_data, engine, filter_doc=t2sql.triples_json_filter_func,
                            value_mapping_func=lambda x, name: x, count_mode=True)
        pbar = tqdm(total=total, colour="#FFA500")
        json_to_sql(name, triples_data, engine, filter_doc=t2sql.triples_json_filter_func,
                    value_mapping_func=lambda x, name: x, pbar=pbar)

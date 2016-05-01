import json
import os
import sqlite3
import time


EDAT_PROJECT_EXTENSION = '.edat'
CONFIG_EXTENSION = '.config'

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def get_json_representation(data_dict):
    return json.dumps(data_dict)


def load_json_file(json_file):
    with open(json_file) as f:
        json_content = load_json(f.read())
        return json_content


def load_json(json_string):
    return json_loads_byteified(json_string)


def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )


def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data


# Privacy Models
K_PRIVACY_MODEL = 'k'
L_PRIVACY_MODEL = 'l'

# Date types
BASIC_TYPE_STRING = 'string'
BASIC_TYPE_INT = 'int'
BASIC_TYPE_DATE = 'date'


def mapping_types(str_type):
    type_d = {
        BASIC_TYPE_STRING: str,
        BASIC_TYPE_INT: int,
        BASIC_TYPE_DATE: str,
    }
    if str_type in type_d.keys():
        return type_d[str_type]
    return str_type


# Privacy Types
PRIVACY_TYPE_IDENTIFIER = 'Identifier'
PRIVACY_TYPE_QI = 'Quasi-Identifier'
PRIVACY_TYPE_SENSITIVE = 'Sensitive'
PRIVACY_TYPE_NON_SENSITIVE = 'Non-Sensitive'

# Hierarchy Types
HIERARCHY_TYPE_GENERALIZATION = 'Generalizaton'
HIERARCHY_TYPE_SUPPRESSION = 'Suppression'

ANONYMIZATION_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anonymization')
ANONYMIZATION_DB_NAME = 'anonymizationDB.db'
ANONYMIZED_DATA_TABLE = 'anonymizedData'
ADDITIONAL_INFO_TABLE = 'additionalInformation'


def create_db(db_name):
    if not os.path.exists(ANONYMIZATION_DIRECTORY):
        os.mkdir(ANONYMIZATION_DIRECTORY)

    with sqlite3.connect(os.path.join(ANONYMIZATION_DIRECTORY, db_name)) as conn:
        cursor = conn.cursor()


def get_anonymization_db_location(db_name=ANONYMIZATION_DB_NAME, create_if_not_exists=True):
    if create_if_not_exists:
        create_db(db_name)
    return os.path.join(ANONYMIZATION_DIRECTORY, db_name)


def timeit_decorator(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '[**] %r %2.2f sec' % (method.__name__, te-ts)
        return result

    return timed

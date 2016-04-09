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
    return json.loads(json_string)

# Privacy Models
K_PRIVACY_MODEL = 'k'
L_PRIVACY_MODEL = 'l'

# Date types
BASIC_TYPE_STRING = 'string'
BASIC_TYPE_INT = 'int'
BASIC_TYPE_DATE = 'date'

# Privacy Types
PRIVACY_TYPE_IDENTIFIER = 'Identifier'
PRIVACY_TYPE_QI = 'Quasi-Identifier'
PRIVACY_TYPE_SENSITIVE = 'Sensitive'
PRIVACY_TYPE_NON_SENSITIVE = 'Non-Sensitive'


ANONYMIZATION_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anonymization')
ANONYMIZATION_DB_NAME = 'anonymizationDB.db'
ANONYMIZED_DATA_TABLE = 'anonymizedData'


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

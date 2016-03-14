import json
import os
import sqlite3


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


BASIC_TYPE_STRING = 'string'
BASIC_TYPE_INT = 'int'
BASIC_TYPE_DATE = 'date'

PRIVACY_TYPE_QI = 'Quasi-Identifier'
PRIVACY_TYPE_IDENTIFIER = 'Identifier'
PRIVACY_TYPE_SENSITIVE = 'Sensitive'
PRIVACY_TYPE_NON_SENSITIVE = 'Non-Sensitive'


ANONYMIZATION_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anonymization')
ANONYMIZATION_DB_NAME = 'anonymizationDB.db'


def create_anonymization_db():
    with sqlite3.connect(os.path.join(ANONYMIZATION_DIRECTORY, ANONYMIZATION_DB_NAME)) as conn:
        cursor = conn.cursor()


def get_anonymization_db_location(create_if_not_exists=True):
    if create_if_not_exists:
        create_anonymization_db()
    return os.path.join(ANONYMIZATION_DIRECTORY, ANONYMIZATION_DB_NAME)



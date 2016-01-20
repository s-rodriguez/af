import json

EDAT_PROJECT_EXTENSION = '.edat'
CONFIG_EXTENSION = '.config'

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def get_json_representation(data_dict):
    return json.dumps(data_dict, sort_keys=True, indent=2)


def load_json_file(json_file):
    with open(json_file) as f:
        json_content = load_json(f.read())
        return json_content


def load_json(json_string):
    return json.loads(json_string)

# TODO REVIEW!
BASIC_TYPE_STRING = 'string'
BASIC_TYPE_INT = 'int'
BASIC_TYPE_DATE = 'date'

PRIVACY_TYPE_1 = 1
PRIVACY_TYPE_2 = 2
# TODO REVIEW!

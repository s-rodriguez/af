import os
from af.model.Attribute import Attribute
import af.utils as utils
from af.exceptions import ImportException


class DataConfig:
    JSON_KEY = 'data_config'

    def __init__(self, project, location=None, data_type=None, table=None, attributes_list=None):
        self.project = project
        self.location = location
        self.type = data_type
        self.table = table
        self.attributes_list = attributes_list if attributes_list is not None else []

    def config_representation(self):
        config = {
            'location': self.location,
            'data_type': self.type,
            'table': self.table,
            'attributes': [attribute.get_representation() for attribute in self.attributes_list],
        }
        return utils.get_json_representation(config)

    def load_config(self, json_string):
        config_dict = utils.load_json(json_string)
        self.validate_config_to_load(config_dict)
        self.location = config_dict['location']
        self.type = config_dict['data_type']
        self.table = config_dict['table']
        for attribute_config in config_dict['attributes']:
            self.attributes_list.append(Attribute(**attribute_config))

    def validate_config_to_load(self, config_dict):
        errors = []
        if not os.path.isfile(config_dict['location']):
            errors.append('Cannot find location of database')

        if len(errors) > 0:
            raise ImportException('\n'.join(errors))

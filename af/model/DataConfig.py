import os

from af.exceptions import ImportException
from af.model.Attribute import Attribute
import af.utils as utils


class DataConfig:
    JSON_KEY = 'data_config'

    def __init__(self, project=None, location=None, data_type=None, table=None, attributes_list=None, anonymized_db_location=None, anonymized_table=None, metrics_table=None):
        self.project = project
        self.location = location
        self.type = data_type
        self.table = table
        self.attributes_list = attributes_list if attributes_list is not None else []
        self.anonymized_db_location = anonymized_db_location
        self.anonymized_table = anonymized_table
        self.metrics_table = metrics_table

    def config_representation(self, json_repr=True):
        config = {
            'location': self.location,
            'data_type': self.type,
            'table': self.table,
            'attributes': [attribute.get_representation() for attribute in self.attributes_list],
            'anonymized_db_location': self.anonymized_db_location,
            'anonymized_table': self.anonymized_table,
            'metrics_table': self.metrics_table
        }
        if json_repr:
            return utils.get_json_representation(config)
        return config

    def load_config(self, data_configuration, from_json=True):
        if from_json:
            config_dict = utils.load_json(data_configuration)
        else:
            config_dict = data_configuration

        self.validate_config_to_load(config_dict)
        self.location = config_dict['location']
        self.type = config_dict['data_type']
        self.table = config_dict['table']
        for attribute_config in config_dict['attributes']:
            self.attributes_list.append(Attribute(**attribute_config))
        self.anonymized_db_location = config_dict['anonymized_db_location']
        self.anonymized_table = config_dict['anonymized_table']
        self.metrics_table = config_dict['metrics_table']

    def validate_config_to_load(self, config_dict):
        errors = []
        if not os.path.isfile(config_dict['location']):
            errors.append('Cannot find location of database')

        if len(errors) > 0:
            raise ImportException('\n'.join(errors))

    def get_privacy_type_attributes_list(self, privacy_type=utils.PRIVACY_TYPE_QI):
        return [attribute for attribute in self.attributes_list if attribute.privacy_type == privacy_type]

    def get_normal_type_attributes_list(self):
        return [attribute for attribute in self.attributes_list if attribute.privacy_type not in (utils.PRIVACY_TYPE_IDENTIFIER, utils.PRIVACY_TYPE_QI)]

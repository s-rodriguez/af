from af.model.Attribute import Attribute
import af.utils as utils


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
            'attributes': [attribute.get_json_representation() for attribute in self.attributes_list],
        }
        return utils.get_json_representation(config)

    def load_config(self, json_string):
        config_dict = utils.load_json(json_string)
        self.location = config_dict['location']
        self.type = config_dict['data_type']
        self.table = config_dict['table']
        for attribute_config in config_dict['attributes']:
            self.attributes_list.append(Attribute(**attribute_config))

    def mock_attributes(self):
        attr_id = Attribute('Id', utils.BASIC_TYPE_INT, utils.PRIVACY_TYPE_1, None)
        attr_name = Attribute('Name', utils.BASIC_TYPE_STRING, utils.PRIVACY_TYPE_1, None)
        attr_price = Attribute('Price', utils.BASIC_TYPE_INT, utils.PRIVACY_TYPE_1, None)

        return [attr_id, attr_name, attr_price]

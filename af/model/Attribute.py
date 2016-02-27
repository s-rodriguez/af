from af.model.transformation_techniques.TransformationTechnique import TransformationTechnique
from af.utils import load_json


class Attribute(object):

    def __init__(self, name=None, basic_type='string', privacy_type=None, transformation_technique=None):
        self.name = name
        self.basic_type = basic_type
        self.privacy_type = privacy_type
        self.transformation_technique = self.set_transformation_technique(transformation_technique)

    def get_json_representation(self):
        return {
            'name': self.name,
            'basic_type': self.basic_type,
            'privacy_type': self.privacy_type,
            'transformation_technique': self.get_transformation_technique_representation()
        }

    def load_config(self, attribute_config):
        config_dict = load_json(attribute_config)
        self.name = config_dict['name']
        self.basic_type = config_dict['basic_type']
        self.privacy_type = config_dict['privacy_type']
        self.set_transformation_technique(config_dict['transformation_technique'])

    def get_transformation_technique_representation(self):
        if self.transformation_technique is not None:
            return self.transformation_technique.get_json_representation()
        else:
            return None

    def set_transformation_technique(self, technique):
        self.transformation_technique = None
        if technique is not None:
            self.transformation_technique = TransformationTechnique.load_technique(technique, self.basic_type)

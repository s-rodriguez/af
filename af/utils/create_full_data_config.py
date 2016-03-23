import os

from af import af_directory

from af.controller.hierarchies.BaseHierarchyController import BaseHierarchyController

from af.model.Attribute import Attribute
from af.model.DataConfig import DataConfig
from af.model.hierarchies.BaseHierarchy import BaseHierarchy

import af.utils as utils


supression_node = BaseHierarchy.supression_node().value

# HIERARCHIES DICTIONARIES REPRESENTATIONS
ssn_hierarchy_dict = {supression_node: None}

race_hierarchy_dict = {
                    supression_node: {
                        'black': None,
                        'white': None
                    }
                }



gender_hierarchy_dict = {
                    supression_node: {
                        'person': {
                            'female': None,
                            'male': None
                        }
                    }
                }


zip_hierarchy_dict = {
                    supression_node: {
                        '021**': {
                            '0214*': {
                                '02141': None,
                            },
                            '0213*': {
                                '02138': None,
                                '02139': None,
                            },
                        }
                    }
                }

year_of_birth_hierarchy_dict = {
                    supression_node: {
                        '**/**/1964': {
                            '5/**/1964': {
                                '5/5/1964': None,
                            },
                            '8/**/1964': {
                                '8/13/1964': None,
                            },
                            '10/**/1964': {
                                '10/23/1964': None,
                            },
                            '11/**/1964': {
                                '11/7/1964': None,
                            },
                            '12/**/1964': {
                                '12/1/1964': None,
                            },
                        },
                        '**/**/1965': {
                            '2/**/1965': {
                                '2/14/1965': None,
                            },
                            '3/**/1965': {
                                '3/15/1965': None,
                            },
                            '8/**/1965': {
                                '8/24/1965': None,
                            },
                            '9/**/1965': {
                                '9/20/1965': None,
                            },
                            '10/**/1965': {
                                '10/23/1965': None,
                            },
                        },
                        '**/**/1967': {
                            '2/**/1967': {
                                '2/13/1967': None,
                            },
                            '3/**/1967': {
                                '3/21/1967': None,
                            },
                        }
                    }
                }


# HIERARCHIES INSTANCES FOR EACH QI AND IDENTIFIABLE ATTRIBUTES
ssn_hierarchy = BaseHierarchyController(BaseHierarchy()).load_hierarchy(ssn_hierarchy_dict, attribute_type=int)
race_hierarchy = BaseHierarchyController(BaseHierarchy()).load_hierarchy(race_hierarchy_dict, attribute_type=str)
gender_hierarchy = BaseHierarchyController(BaseHierarchy()).load_hierarchy(gender_hierarchy_dict, attribute_type=str)
zip_hierarchy = BaseHierarchyController(BaseHierarchy()).load_hierarchy(zip_hierarchy_dict, attribute_type=str)
year_of_birth_hierarchy = BaseHierarchyController(BaseHierarchy()).load_hierarchy(year_of_birth_hierarchy_dict, attribute_type=str)


# ATTRIBUTE INSTANCES FOR ALL ATTRIBUTES ON TABLE
att_ssn = Attribute('ssn', basic_type='int', privacy_type=utils.PRIVACY_TYPE_IDENTIFIER)
att_ssn.hierarchy = ssn_hierarchy

att_race = Attribute('race', privacy_type=utils.PRIVACY_TYPE_QI)
att_race.hierarchy = race_hierarchy

att_year_of_birth = Attribute('birth', privacy_type=utils.PRIVACY_TYPE_QI)
att_year_of_birth.hierarchy = year_of_birth_hierarchy

att_gender = Attribute('gender', privacy_type=utils.PRIVACY_TYPE_QI)
att_gender.hierarchy = gender_hierarchy

att_zip = Attribute('zip', privacy_type=utils.PRIVACY_TYPE_QI)
att_zip.hierarchy = zip_hierarchy

att_problem = Attribute('problem', privacy_type=utils.PRIVACY_TYPE_SENSITIVE)


# CREATE DATA CONFIG
attributes_list = [att_ssn, att_race, att_gender, att_zip, att_year_of_birth, att_problem]
table = 'sickness'
db_location = os.path.join(af_directory(), 'utils', 'sickness.db')

data_config = DataConfig(location=db_location, data_type='sqlite', table=table, attributes_list=attributes_list)

#print data_config.config_representation()

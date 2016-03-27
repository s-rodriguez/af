import os
import sqlite3

from af import af_directory

from af.controller.hierarchies.BaseHierarchyController import BaseHierarchyController

from af.model.Attribute import Attribute
from af.model.DataConfig import DataConfig
from af.model.hierarchies.BaseHierarchy import BaseHierarchy

import af.utils as utils
import af.utils.automatic_dimensions as automatic_dimensions
import af.utils.create_sickness_db as create_sickness_db


db_directory, db_name = create_sickness_db.get_directory_and_db_name()
if not os.path.isfile(os.path.join(db_directory, db_name)):
    create_sickness_db.create_db()


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

with sqlite3.connect(os.path.join(db_directory, db_name)) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT(zip) FROM SICKNESS")
    zip_results = [str(v[0]) for v in cursor.fetchall()]
    zip_automatic = automatic_dimensions.IntPartialSupressionRightToLeft(zip_results, 1)
    zip_hierarchy_dict = zip_automatic.create_dimensions()

    cursor.execute("SELECT DISTINCT(birth) FROM SICKNESS")
    birth_results = [str(v[0]) for v in cursor.fetchall()]
    birth_automatic = automatic_dimensions.DatePartialSupressionDDMMYYYY(birth_results)
    birth_dimensions = birth_automatic.create_dimensions()
    year_of_birth_hierarchy_dict = {supression_node: birth_dimensions}

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

import os
import sqlite3

from af import af_directory
from af.controller.hierarchies.BaseHierarchyController import BaseHierarchyController
import af.controller.hierarchies.AutomaticDimension as AutomaticDimension
from af.model.Attribute import Attribute
from af.model.DataConfig import DataConfig
from af.model.hierarchies.BaseHierarchy import BaseHierarchy
import af.utils as utils
import af.utils.create_sickness_db as create_sickness_db

db_directory, db_name = create_sickness_db.get_directory_and_db_name()
if not os.path.isfile(os.path.join(db_directory, db_name)):
    create_sickness_db.create_db(db_directory, db_name)


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

city_hierarchy_dict = {
                    supression_node: {
                        'Argentina': {
                            'Buenos Aires': {
                                'La Plata': None,
                                'Mar del Plata': None,
                                'Avellaneda': None,
                                'Ciudad de Buenos Aires': None,
                                'La Matanza': None,
                                'San Martin': None,
                                'Bahia Blanca': None,
                                'Tandil': None,
                                'Pergamino': None,
                            },
                            'Santa Fe': {
                                'Rosario': None,
                                'Santa Fe Cap': None,
                                'Reconquista': None,
                                'Rafaela': None,
                                'Firmat': None,
                                'Sunchales': None,
                            },
                            'Entre Rios': {
                                'Parana': None,
                                'Gualeguay': None,
                                'Gualeguaychu': None,
                                'Victoria': None,
                                'Colon': None,
                                'Concepcion del Uruguay': None,
                            },
                            'Cordoba': {
                                'Cordoba Cap': None,
                                'Sierra de los Padres': None,
                                'Mina Clavero': None,
                                'Rio Cuarto': None,
                                'Rio Tercero': None,
                                'Villa Gral Belgrano': None,
                            },
                            'Mendoza': {
                                'Mendoza Cap': None,
                                'San Rafael': None,
                                'Malargue': None,
                                'Las Heras': None,
                                'Guaymallen': None,
                                'Maipu': None,
                            },
                            'Salta': {
                                'Salta Cap': None,
                                'Cachi': None,
                                'Cafayate': None,
                                'Iruya':None,
                                'Tartagal': None,
                                'Angastaco': None,
                            },
                        }
                    }
                }

profession_hierarchy_dict = {
                    supression_node: {
                        'Professional': {
                            'Medicine': {
                                'Endocrinology': None,
                                'Cardiology': None,
                                'Geriatrics': None,
                                'Paediatrics': None,
                                'Neurology': None,
                                'Radiology': None,
                            },
                            'Law': {
                                'Civil Attorney': None,
                                'Criminal Attorney': None,
                                'Employment Attorney': None,
                                'Family Attorney':None,
                                'Administrative Attorney':None,
                            },
                            'Engineering': {
                                'Civil Engineering': None,
                                'Chemical Engineering': None,
                                'Software Engineering': None,
                                'Mechanical Engineering': None,
                                'Industrial Engineering': None,
                            },
                            'Science': {
                                'Mathematician': None,
                                'Biologist': None,
                                'Physicist': None,
                                'Chemist': None,
                                'Geologist': None,
                            },
                        },
                        'No professional': {
                            'Trade': {
                                'Plumber': None,
                                'Electrician': None,
                                'Carpenter': None,
                                'Shoemaker': None,
                                'Blacksmith': None,
                                'Builder': None,
                            }
                        }
                    }
                }


with sqlite3.connect(os.path.join(db_directory, db_name)) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT(zip) FROM SICKNESS")
    zip_results = [str(v[0]) for v in cursor.fetchall()]
    zip_automatic = AutomaticDimension.PartialSupressionRightToLeft(zip_results, 1)
    zip_hierarchy_dict = zip_automatic.create_dimensions()

    cursor.execute("SELECT DISTINCT(birth) FROM SICKNESS")
    birth_results = [str(v[0]) for v in cursor.fetchall()]
    birth_automatic = AutomaticDimension.DatePartialSupressionDDMMYYYY(birth_results)
    birth_dimensions = birth_automatic.create_dimensions()
    year_of_birth_hierarchy_dict = birth_automatic.create_dimensions()

# HIERARCHIES INSTANCES FOR EACH QI AND IDENTIFIABLE ATTRIBUTES
ssn_hierarchy = BaseHierarchyController(BaseHierarchy()).load_hierarchy(ssn_hierarchy_dict, attribute_type=int)
race_hierarchy = BaseHierarchyController(BaseHierarchy()).load_hierarchy(race_hierarchy_dict, attribute_type=str)
gender_hierarchy = BaseHierarchyController(BaseHierarchy()).load_hierarchy(gender_hierarchy_dict, attribute_type=str)
zip_hierarchy = BaseHierarchyController(BaseHierarchy()).load_hierarchy(zip_hierarchy_dict, attribute_type=str)
year_of_birth_hierarchy = BaseHierarchyController(BaseHierarchy()).load_hierarchy(year_of_birth_hierarchy_dict, attribute_type=str)
city_hierarchy = BaseHierarchyController(BaseHierarchy()).load_hierarchy(city_hierarchy_dict, attribute_type=str)
profession_hierarchy = BaseHierarchyController(BaseHierarchy()).load_hierarchy(profession_hierarchy_dict, attribute_type=str)


# ATTRIBUTE INSTANCES FOR ALL ATTRIBUTES ON TABLE
att_ssn = Attribute('SSN', basic_type='int', privacy_type=utils.PRIVACY_TYPE_IDENTIFIER)
att_ssn.hierarchy = ssn_hierarchy

att_race = Attribute('RACE', privacy_type=utils.PRIVACY_TYPE_QI)
att_race.hierarchy = race_hierarchy

att_year_of_birth = Attribute('BIRTH', privacy_type=utils.PRIVACY_TYPE_QI, weight=2)
att_year_of_birth.hierarchy = year_of_birth_hierarchy

att_gender = Attribute('GENDER', privacy_type=utils.PRIVACY_TYPE_QI)
att_gender.hierarchy = gender_hierarchy

att_zip = Attribute('ZIP', privacy_type=utils.PRIVACY_TYPE_QI, weight=4)
att_zip.hierarchy = zip_hierarchy

att_city = Attribute('CITY', privacy_type=utils.PRIVACY_TYPE_QI, weight=3)
att_city.hierarchy = city_hierarchy

att_profession = Attribute('PROFESSION', privacy_type=utils.PRIVACY_TYPE_QI, weight=3)
att_profession.hierarchy = profession_hierarchy

att_problem = Attribute('PROBLEM', privacy_type=utils.PRIVACY_TYPE_SENSITIVE)


# CREATE DATA CONFIG
attributes_list = [att_ssn, att_race, att_gender, att_zip, att_year_of_birth, att_city, att_profession, att_problem]
table = 'sickness'
db_location = os.path.join(db_directory, db_name)

data_config = DataConfig(project='sickness_project', location=db_location, data_type='sqlite', table=table, attributes_list=attributes_list)

#print data_config.config_representation()

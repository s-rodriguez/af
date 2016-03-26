from random import randint
import sqlite3
import os
from af import af_directory

from af.controller.hierarchies.BaseHierarchyController import BaseHierarchyController

from af.model.Attribute import Attribute
from af.model.DataConfig import DataConfig
from af.model.hierarchies.BaseHierarchy import BaseHierarchy

import af.utils as utils
from af.model.algorithms.Datafly import Datafly
from af.model.algorithms.IncognitoK import IncognitoK



# DB Creation
conn = sqlite3.connect('sicknesslarge.db')
print "Opened database successfully";

conn.execute('''CREATE TABLE sickness
       (SSN INT,
       RACE           CHAR(12)    NOT NULL,
       BIRTH           CHAR(12)    NOT NULL,
       GENDER        CHAR(12),
       ZIP         CHAR(6),
       PROBLEM        CHAR(20));''')
print "Table created successfully";

race = ['female', 'male']
gender = ['black', 'white']
birth = ['2/13/1967', '3/21/1967', '5/5/1967', '8/27/1967', '11/27/1967', '12/3/1967',
         '2/14/1965', '3/15/1965', '8/24/1965', '9/20/1965', '10/23/1965', '12/8/1965',
         '1/30/1964', '5/5/1964', '8/13/1964', '10/23/1964', '11/7/1964', '12/1/1964', ]
zip = range(2130, 2179)
problem = ['hiv', 'cancer', 'short of breath', 'chest pain', 'painful eye',
           'wheezing', 'obesity', 'hypertension', 'fever', 'vomiting', 'flu']

i = 0
while i < 1000:
    r = race[randint(0, 1)]
    g = gender[randint(0, 1)]
    b = birth[randint(0, len(birth) - 1)]
    z = zip[randint(0, len(zip) - 1)]
    p = problem[randint(0, len(problem) - 1 )]
    i += 1
    query = "INSERT INTO SICKNESS VALUES ( ?, ?, ?, ?, ?, ?)"
    conn.execute(query, (i, r, b, g, z, p))

conn.commit()
conn.close()
# ============================================================================

# Data Config Creation
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
                        '21**': {
                            '217*': {
                                '2170': None,
                                '2171': None,
                                '2172': None,
                                '2173': None,
                                '2174': None,
                                '2175': None,
                                '2176': None,
                                '2177': None,
                                '2178': None,
                                '2179': None,
                            },
                            '216*': {
                                '2160': None,
                                '2161': None,
                                '2162': None,
                                '2163': None,
                                '2164': None,
                                '2165': None,
                                '2166': None,
                                '2167': None,
                                '2168': None,
                                '2169': None,
                            },
                            '215*': {
                                '2150': None,
                                '2151': None,
                                '2152': None,
                                '2153': None,
                                '2154': None,
                                '2155': None,
                                '2156': None,
                                '2157': None,
                                '2158': None,
                                '2159': None,
                            },
                            '214*': {
                                '2140': None,
                                '2141': None,
                                '2142': None,
                                '2143': None,
                                '2144': None,
                                '2145': None,
                                '2146': None,
                                '2147': None,
                                '2148': None,
                                '2149': None,
                            },
                            '213*': {
                                '2130': None,
                                '2131': None,
                                '2132': None,
                                '2133': None,
                                '2134': None,
                                '2135': None,
                                '2136': None,
                                '2137': None,
                                '2138': None,
                                '2139': None,
                            },
                            '212*': {
                                '2120': None,
                                '2121': None,
                                '2122': None,
                                '2123': None,
                                '2124': None,
                                '2125': None,
                                '2126': None,
                                '2127': None,
                                '2128': None,
                                '2129': None,
                            },
                            '211*': {
                                '2110': None,
                                '2111': None,
                                '2112': None,
                                '2113': None,
                                '2114': None,
                                '2115': None,
                                '2116': None,
                                '2117': None,
                                '2118': None,
                                '2119': None,
                            },
                            '210*': {
                                '2100': None,
                                '2101': None,
                                '2102': None,
                                '2103': None,
                                '2104': None,
                                '2105': None,
                                '2106': None,
                                '2107': None,
                                '2108': None,
                                '2109': None,
                            },
                        }
                    }
                }

year_of_birth_hierarchy_dict = {
                    supression_node: {
                        '**/**/1964': {
                            '1/**/1964': {
                                '1/30/1964': None,
                            },
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
                            '12/**/1965': {
                                '12/8/1965': None,
                            },
                        },
                        '**/**/1967': {
                            '2/**/1967': {
                                '2/13/1967': None,
                            },
                            '3/**/1967': {
                                '3/21/1967': None,
                            },
                            '5/**/1967': {
                                '5/5/1967': None,
                            },
                            '8/**/1967': {
                                '8/27/1967': None,
                            },
                            '11/**/1967': {
                                '11/27/1967': None,
                            },
                            '12/**/1967': {
                                '12/3/1967': None,
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
db_location = os.path.join(af_directory(), 'utils', 'sicknesslarge.db')

data_config = DataConfig(location=db_location, data_type='sqlite', table=table, attributes_list=attributes_list)

# d = Datafly(data_config, 10)
# d.anonymize()

# i = IncognitoK(data_config, 4)
# i.anonymize()

os.remove('sicknesslarge.db')
# ============================================================================

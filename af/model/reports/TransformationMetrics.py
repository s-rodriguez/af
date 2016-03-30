from af.controller.data.SqliteController import SqliteController
from af.utils import (
    get_anonymization_db_location,
    ANONYMIZED_DATA_TABLE,
    PRIVACY_TYPE_QI,
)


class TransformationMetrics(object):

    def __init__(self, data_config):
        self.data_config = data_config
        self.qi_attributes = data_config.get_privacy_type_attributes_list(PRIVACY_TYPE_QI)

        self.original_db = SqliteController(self.data_config.location)
        self.original_db_table = self.data_config.table

        self.anonymized_db = SqliteController(get_anonymization_db_location())
        self.anonymized_db_table = ANONYMIZED_DATA_TABLE

    def qi_eq_classes_differences(self):
        eq_classes = {}
        dbs = (self.original_db, self.anonymized_db)
        tables = (self.original_db_table, self.anonymized_db_table)

        for qi_att in self.qi_attributes:
            amounts = []
            for db, table in zip(dbs, tables):
                amounts.extend(list(db.get_count_of_distinct_qi_values(table , qi_att.name)))
            eq_classes[qi_att.name] = tuple(amounts)

        return eq_classes

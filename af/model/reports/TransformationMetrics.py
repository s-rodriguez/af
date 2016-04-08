from af.controller.data.SqliteController import SqliteController
from af.utils import (
    get_anonymization_db_location,
    ANONYMIZED_DATA_TABLE,
    PRIVACY_TYPE_QI,
)


class TransformationMetrics(object):

    def __init__(self, data_config, additional_information):
        self.data_config = data_config
        self.additional_information = additional_information

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
                amounts.extend(list(db.get_count_of_distinct_qi_values(table, qi_att.name)))
            eq_classes[qi_att.name] = tuple(amounts)

        return eq_classes

    def removed_outlier_rows(self):
        dbs = (self.original_db, self.anonymized_db)
        tables = (self.original_db_table, self.anonymized_db_table)
        rows_amount = []
        for db, table in zip(dbs, tables):
            rows_amount.append(db.amount_of_rows(table))
        return rows_amount[0] - rows_amount[1]

    def number_of_qi_eq_classes_generated(self):
        qi_list = [att.name for att in self.qi_attributes]
        return self.anonymized_db.get_frequency_of_eq_classes(self.anonymized_db_table, qi_list)

    def qi_eq_classes_generated(self):
        qi_list = [att.name for att in self.qi_attributes]
        for value in self.anonymized_db.get_frequency_of_qi_attributes(self.anonymized_db_table, qi_list):
            yield value




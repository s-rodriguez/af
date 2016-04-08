from jinja2 import Environment, FileSystemLoader
import os

from af import (
    af_directory,
    af_user_directory,
    utils,
)
from af.controller.data.SqliteController import SqliteController



def get_report_location_output(report_name):
    return os.path.join(af_user_directory(), 'reports', report_name)


def get_templates_location():
    return os.path.join(af_directory(), 'templates')


def get_anonymized_sample(data_config):
    anon_db_controller = SqliteController(utils.get_anonymization_db_location())
    anonymization_table = utils.ANONYMIZED_DATA_TABLE
    qi_list = [att.name for att in data_config.get_privacy_type_attributes_list()]
    return anon_db_controller.get_groups_examples(anonymization_table, qi_list)


def create_basic_report(transformation_metrics, template_name='my_report.html'):
    env = Environment(loader=FileSystemLoader(get_templates_location()))
    template = env.get_template(template_name)
    anonymized_sample = get_anonymized_sample(transformation_metrics.data_config)

    template_vars = {
        "eq_classes_differences" : transformation_metrics.qi_eq_classes_differences(),
        "removed_outliers": transformation_metrics.removed_outlier_rows(),
        "eq_classes_amount": transformation_metrics.number_of_qi_eq_classes_generated(),
        "additional_information": transformation_metrics.additional_information,
        "anonymized_sample": anonymized_sample,
    }

    html_out = template.render(template_vars)
    report_location = get_report_location_output(template_name)
    with open(report_location, 'w+') as f:
        f.write(html_out)

    return report_location

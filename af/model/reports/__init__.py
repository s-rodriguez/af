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


def get_js_location(js_file_name):
    return os.path.join(af_directory(), 'js', js_file_name)


def get_processed_eq_classes_differences_for_chart(eq_classes_differences):
    categories = []
    before_data = []
    after_data = []

    for att_name, values in eq_classes_differences.iteritems():
        categories.append(att_name)
        before_data.append(values[0])
        after_data.append(values[1])

    return {
        'categories': categories,
        'before': before_data,
        'after': after_data
    }

def get_anonymized_sample(data_config):
    anon_db_controller = SqliteController(utils.get_anonymization_db_location())
    anonymization_table = utils.ANONYMIZED_DATA_TABLE
    qi_list = [att.name for att in data_config.get_privacy_type_attributes_list()]
    return anon_db_controller.get_groups_examples(anonymization_table, qi_list)


def create_basic_report(transformation_metrics, template_name='my_report.html', report_name='my_report', convert_to_pdf=False):
    env = Environment(loader=FileSystemLoader(get_templates_location()))
    template = env.get_template(template_name)
    anonymized_sample = get_anonymized_sample(transformation_metrics.data_config)
    eq_classes_differences = transformation_metrics.qi_eq_classes_differences()
    eq_classes_differences_chart = get_processed_eq_classes_differences_for_chart(eq_classes_differences)

    template_vars = {
        "eq_classes_differences" : eq_classes_differences,
        "eq_classes_differences_chart": eq_classes_differences_chart,
        "removed_outliers": transformation_metrics.removed_outlier_rows(),
        "eq_classes_amount": transformation_metrics.number_of_qi_eq_classes_generated(),
        "additional_information": transformation_metrics.additional_information,
        "anonymized_sample": anonymized_sample,
        "highcharts_location": get_js_location('highcharts.js'),
        "jquery_location": get_js_location('jquery-1.12.3.min.js')
    }

    html_out = template.render(template_vars)
    report_location = get_report_location_output(report_name+'.html')
    with open(report_location, 'w+') as f:
        f.write(html_out)

    if convert_to_pdf:
        import pdfkit
        pdf_output = get_report_location_output(report_name+'.pdf')
        pdfkit.from_file(report_location, pdf_output)

    return report_location

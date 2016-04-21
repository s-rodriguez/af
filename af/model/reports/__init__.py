from jinja2 import Environment, FileSystemLoader
import os
import pdfkit


from af import (
    af_directory,
    af_user_directory,
    utils,
)
from af.controller.data.SqliteController import SqliteController


def get_report_location_output(report_name):
    """Return the full report location.

    :param string report_name: Name of the report
    :rtype: Full location of the report

    """
    return os.path.join(af_user_directory(), 'reports', report_name)


def get_templates_location():
    """Return the location of the templates directory

    :rtype: Path to the templates directory

    """
    return os.path.join(af_directory(), 'model', 'reports', 'templates')


def get_list_of_deletable_attributes_for_pdf():
    """When exporting to PDF, some things should be deleted, like things that have a certain behaviour based on jquery

    :rtype: Tuple containing all the strings to look and remove from the html output

    """
    return (
        "<input type='button' value='-' id='PlusMinus'/>",
    )


def get_anonymized_sample(data_config):
    """Return a sample of the anonymization data

    :param data_config: Instance of class DataConfig
    :rtype: List sample of anonymized data

    """
    anon_db_controller = SqliteController(utils.get_anonymization_db_location())
    anonymization_table = utils.ANONYMIZED_DATA_TABLE
    qi_list = [att.name for att in data_config.get_privacy_type_attributes_list()]
    return anon_db_controller.get_groups_examples(anonymization_table, qi_list)


def create_basic_report(transformation_metrics, template_name='my_report.html', report_location_path=None, convert_to_format='html'):
    """Create a basic report

    :param transformation_metrics: Instance of the TransformationMetrics class
    :param string template_name: Template to use
    :param string report_location_path: Custom location where we want to export the report
    :param string convert_to_format: Indicates to which format the report should be exported. (HTML by default)
    :rtype: String location of the created report

    """
    env = Environment(loader=FileSystemLoader(get_templates_location()))
    template = env.get_template(template_name)
    anonymized_sample = get_anonymized_sample(transformation_metrics.data_config)
    eq_classes_differences = transformation_metrics.qi_eq_classes_differences()

    template_vars = {
        "eq_classes_differences" : eq_classes_differences,
        "removed_outliers": transformation_metrics.removed_outlier_rows(),
        "eq_classes_amount": transformation_metrics.number_of_qi_eq_classes_generated(),
        "additional_information": transformation_metrics.additional_information,
        "anonymized_sample": anonymized_sample,
    }

    html_out = template.render(template_vars)

    if report_location_path is None:
        report_location_path = get_report_location_output('my_report')

    report_location_path_html = report_location_path + '.html'
    with open(report_location_path_html, 'w+') as f:
        f.write(html_out)

    if convert_to_format.lower() == 'pdf':
        convert_report_to_pdf(html_out, report_location_path)
        os.remove(report_location_path_html)
        return report_location_path + '.pdf'

    return report_location_path_html


def convert_report_to_pdf(html_string, report_name):
    """Given a html output, and a report name, convert it to a pdf

    :param string html_string: An HTML output
    :param string report_name: Name of the final report

    """
    for deletable in get_list_of_deletable_attributes_for_pdf():
        html_string = html_string.replace(deletable, '')
    pdf_output = get_report_location_output(report_name+'.pdf')
    pdfkit.from_string(html_string, pdf_output)

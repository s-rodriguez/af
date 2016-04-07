from jinja2 import Environment, FileSystemLoader
import os

from af import (
    af_directory,
    af_user_directory,
)
from af.model.reports.TransformationMetrics import TransformationMetrics


def get_report_location_output(report_name):
    return os.path.join(af_user_directory(), 'reports', report_name)


def get_templates_location():
    return os.path.join(af_directory(), 'templates')


def create_basic_report(data_config, template_name='my_report.html'):
    env = Environment(loader=FileSystemLoader(get_templates_location()))
    template = env.get_template(template_name)

    tm = TransformationMetrics(data_config)

    template_vars = {
        "eq_classes_differences" : tm.qi_eq_classes_differences(),
    }

    html_out = template.render(template_vars)
    report_location = get_report_location_output(template_name)
    with open(report_location, 'w+') as f:
        f.write(html_out)

    return report_location

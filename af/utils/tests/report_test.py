from af.model.reports.TransformationMetrics import TransformationMetrics


def report_test():
    from af.utils import create_full_data_config
    dc = create_full_data_config.data_config
    tm = TransformationMetrics(dc)
    from af.model.reports import create_basic_report
    location = create_basic_report(tm, convert_to_pdf=True)
    print "Reporte creado en: %s" % location


if __name__ == "__main__":
    report_test()

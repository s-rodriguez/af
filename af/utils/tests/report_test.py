from af.model.reports.TransformationMetrics import TransformationMetrics


def report_test():
    from af.utils import create_full_data_config
    dc = create_full_data_config.data_config
    additional_info = {
        1: ('Anonymization Duration', '5.44 seconds'),
        2: ('Model Conditions', 'K: 2'),
        3: ('Selected Hierarchy Levels', {'city': 2, 'zip': 4, 'gender': 0, 'profession': 1, 'race': 0, 'birth': 3}),
        5: ('Other Possible Hierarchy Levels', [{'city': 2, 'zip': 4, 'gender': 0, 'profession': 1, 'race': 0, 'birth': 3}, {'city': 1, 'zip': 4, 'gender': 0, 'profession': 3, 'race': 0, 'birth': 3},])
    }
    tm = TransformationMetrics(dc, additional_info)
    from af.model.reports import create_basic_report
    location = create_basic_report(tm)
    print "Reporte creado en: %s" % location


if __name__ == "__main__":
    report_test()

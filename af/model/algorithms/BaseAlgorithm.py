class BaseAlgorithm(object):

    def __init__(self, data_config):
        self.data_config = data_config
        self.anonymization_table = None
        self.input_table = None
        self.attributes = data_config.attributes_list

    def anonymize(self):
        pass

    def validate_anonymize_conditions(self):
        pass

    def input_preprocessing(self):
        pass

    def read_input_table(self):
        # this method should be implemented here
        pass

    def write_ouput_table(self):
        # this method should be implemented here
        pass

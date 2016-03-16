from af.model.algorithms.BaseKAlgorithm import BaseKAlgorithm

class Datafly(BaseKAlgorithm):

    def __init__(self, data_config):
        BaseKAlgorithm.__init__(self, data_config)

    def anonymize(self):
        self.on_pre_process()
        while self.validate_anonymize_conditions(self.attributes) is not True:
            qi_to_anonymize = self.obtain_qi_most_frequently()
            # qi_to_anonymize.transformation_technique.transform(...
        self.on_post_process()



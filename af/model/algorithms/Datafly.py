from af.model.algorithms.BaseKAlgorithm import BaseKAlgorithm

class Datafly(BaseKAlgorithm):

    def __init__(self, data_config):
        BaseKAlgorithm.__init__(self, data_config)

    def anonymize(self):
        self.on_pre_process()
        while self.validate_anonymize_conditions(self.attributes) is not True:
            qi_to_anonymize = self.obtain_qi_most_frequently()
            qi_leaf_nodes = qi_to_anonymize.transform_leaf_nodes()
            for current_value, new_value in qi_leaf_nodes.iteritems():
                self.replace_value(qi_to_anonymize, new_value, current_value)

        self.on_post_process()



from af.model.algorithms.BaseKAlgorithm import BaseKAlgorithm


class IncognitoK(BaseKAlgorithm):

    def __init__(self, data_config):
        BaseKAlgorithm.__init__(self, data_config)
        self.db_original_copy_controller = SqliteController()

    def anonymize(self):
        self.on_pre_process()
        # while self.validate_anonymize_conditions(self.attributes) is not True:
        #     qi_to_anonymize = self.obtain_qi_most_frequently()
        #     # qi_to_anonymize.transformation_technique.transform(...
        self.on_post_process()


    def validate_anonymize_conditions(self):
        pass

    def create_walking_bfs_hierarchy_levels_tree(self):
        pass

    def create_table_hierarchies_star_schema(self):
        pass

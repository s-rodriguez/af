from af.model.transformation_techniques.TransformationTechnique import TransformationTechnique


class GeneralizationTechnique(TransformationTechnique):
    TECHNIQUE_KEY = 'Generalization'

    def transform(self, data_value, lvl=None):
        """Generalize the given data to a higher level
        :param data: intended to be generalized
        """
        data_node = self.hierarchy.get_leaf_node(data_value)
        generalized_node = self.hierarchy.get_generalization_level_representation(data_node, generalization_level)
        return generalized_node.value

    def save_technique(self):
        return {
            'technique_key': self.TECHNIQUE_KEY
        }

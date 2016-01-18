from af.model.transformation_techniques.TransformationTechnique import TransformationTechnique


class SuppressionTechnique(TransformationTechnique):
    TECHNIQUE_KEY = 'Suppression'

    def transform(self, data):
        """Suppress the given data in a complete way
        :param data: intended to be suppress
        """
        return '*'*10

    def save_technique(self):
        return {
            'technique_key': self.TECHNIQUE_KEY
        }

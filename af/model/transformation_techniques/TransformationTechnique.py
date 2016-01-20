import abc


class TransformationTechnique(object):
    __metaclass__ = abc.ABCMeta
    TECHNIQUE_KEY = None

    @abc.abstractmethod
    def transform(self, data):
        """Transform original data using its particular technique
        :param data: intended to be suppress
        """
        return

    def get_json_representation(self):
        """Returns the json representation of the techinque"""
        return {'technique_key': self.TECHNIQUE_KEY}

    @abc.abstractmethod
    def save_technique(self):
        """Get the technique representation to be able to save it"""
        return
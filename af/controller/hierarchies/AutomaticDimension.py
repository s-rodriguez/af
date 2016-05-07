from af.model.hierarchies.BaseHierarchy import BaseHierarchy
from af.utils import (
    BASIC_TYPE_STRING,
    BASIC_TYPE_INT,
    BASIC_TYPE_DATE,
)


class AutomaticDimension(object):
    """Class to create automatic dimensions for the hierarchies

    """

    AD_NAME = ''
    AD_DESCRIPTION = ''
    VALID_FOR_TYPE = ()

    def __init__(self, list_of_values):
        self.set_of_values = set([str(val) for val in list_of_values])

    def create_dimensions(self, dimensions_queue=None):
        if dimensions_queue is None:
            dimensions_queue = [{key: None} for key in self.set_of_values]

        new_dimensions_queue = {}

        for element in dimensions_queue:
            parent = self.get_parent(element.keys()[0])
            if parent not in new_dimensions_queue.keys():
                new_dimensions_queue[parent] = element
            else:
                new_dimensions_queue[parent].update(element)

        if len(new_dimensions_queue) == 1:
            return new_dimensions_queue
        else:
            return self.create_dimensions([{key: value} for key, value in new_dimensions_queue.iteritems()])


class PartialSupressionLeftToRight(AutomaticDimension):

    AD_NAME = 'Left To Right'
    AD_DESCRIPTION = 'Suppresses the values from left to right, with a default of two spaces at a time.\n Example: (123456 -> **3456 -> ****56 -> ******)'
    VALID_FOR_TYPE = (BASIC_TYPE_STRING, BASIC_TYPE_INT)

    def __init__(self, list_of_values, amount_to_supress=2):
        AutomaticDimension.__init__(self, list_of_values)
        self.amount_to_supress = amount_to_supress

    def get_parent(self, value):
        if not '*' in value:
            supressed = ''
            not_supressed = value
        else:
            supressed = value[0:value.rfind('*')+1]
            not_supressed = value[value.rfind('*')+1:]

        if len(supressed) == len(value):
            return value

        to_supress = '*'*self.amount_to_supress
        still_not_supressed = not_supressed[1*self.amount_to_supress:]

        parent = supressed+to_supress+still_not_supressed
        if all('*' == i for i in parent):
            parent = BaseHierarchy.supression_node().value
        return parent


class PartialSupressionRightToLeft(PartialSupressionLeftToRight):

    AD_NAME = 'Right to Left'
    AD_DESCRIPTION = 'Suppresses the values from right to left, with a default of two spaces at a time.\nExample: (123456 -> 1234** -> 12**** -> ******)'
    VALID_FOR_TYPE = (BASIC_TYPE_STRING, BASIC_TYPE_INT)

    def __init__(self, list_of_values, amount_to_supress=2):
        PartialSupressionLeftToRight.__init__(self, list_of_values, amount_to_supress)

    def get_parent(self, value):
        aux = value[::-1]
        result = PartialSupressionLeftToRight.get_parent(self, aux)
        return result [::-1]


class DatePartialSupressionYYYYMMDD(AutomaticDimension):

    AD_NAME = 'YYYY/MM/DD Format'
    AD_DESCRIPTION = 'Suppresses date string formats, from day to year, with the default separator /.\nExample: (2016/03/11 -> 2016/03/** -> 2016/**/** -> ****/**/**'
    VALID_FOR_TYPE = (BASIC_TYPE_DATE,)

    def __init__(self, list_of_values):
        AutomaticDimension.__init__(self, list_of_values)

    def get_parent(self, value):
        year, month, day = value.split('/')
        if '*' not in day:
            day = '**'
        elif '*' not in month:
            month = '**'
        else:
            #Full supression of value
            result = BaseHierarchy.supression_node().value
            return result

        result = "{0}/{1}/{2}".format(year, month, day)
        return result

class DatePartialSupressionDDMMYYYY(DatePartialSupressionYYYYMMDD):

    AD_NAME = 'DD/MM/YYYY Format'
    AD_DESCRIPTION = 'Suppresses date string formats, from day to year, with the default separator /.\nExample: (11/03/2016 -> **/03/2016 -> **/**/2016 -> ****/**/**'
    VALID_FOR_TYPE = (BASIC_TYPE_DATE,)

    def __init__(self, list_of_values):
        DatePartialSupressionYYYYMMDD.__init__(self, list_of_values)

    def get_parent(self, value):
        aux = value[::-1]
        result = DatePartialSupressionYYYYMMDD.get_parent(self, aux)
        return result [::-1]

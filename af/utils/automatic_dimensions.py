from af.model.hierarchies.BaseHierarchy import BaseHierarchy


class AutomaticDimension(object):

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


class IntPartialSupressionLeftToRight(AutomaticDimension):

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


class IntPartialSupressionRightToLeft(IntPartialSupressionLeftToRight):

    def __init__(self, list_of_values, amount_to_supress=2):
        IntPartialSupressionLeftToRight.__init__(self, list_of_values, amount_to_supress)

    def get_parent(self, value):
        aux = value[::-1]
        result = IntPartialSupressionLeftToRight.get_parent(self, aux)
        return result [::-1]


class IntRange(AutomaticDimension):

    def __init__(self, list_of_values, amount_range=10):
        AutomaticDimension.__init__(self, list_of_values)
        self.amount_range = amount_range

    def get_parent(self, value):
        pass


class DatePartialSupression(AutomaticDimension):

    def __init__(self, list_of_values):
        AutomaticDimension.__init__(self, list_of_values)

    def get_parent(self, value):
        pass

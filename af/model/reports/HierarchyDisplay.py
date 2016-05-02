import os

from af import af_directory


class HierarchyDisplay:

    def __init__(self):
        self.template = None
        self.hierarchy = None

    def create_display(self, hierarchy):
        self.hierarchy = hierarchy
        self.template = self.get_hierarchy_template()

        hierarchy_representation = self.hierarchy.create_html_representation()
        self.template = self.template.replace("###HIERARCHY_DISPLAY###", hierarchy_representation)

        return self.template

    def get_hierarchy_template(self):
        html_template = """
        <!DOCTYPE html>
        <html>

        <div id="jstree">
            ###HIERARCHY_DISPLAY###
        </div>

        </html>
        """

        return html_template

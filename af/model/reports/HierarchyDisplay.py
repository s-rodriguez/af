import os

from af import af_directory


class HierarchyDisplay:

    def __init__(self):
        self.template = None
        self.hierarchy = None

    def create_display(self, hierarchy):
        self.hierarchy = hierarchy
        self.template = self.get_hierarchy_template()

        js_path = os.path.abspath(os.path.join(af_directory(), 'model', 'reports', 'javascript'))
        self.template = self.template.replace("###JS_LOCATION_TAG###", js_path)

        hierarchy_representation = self.hierarchy.create_html_representation()
        hierarchy_representation = hierarchy_representation.replace("li", """li data-jstree='{"opened":true}'""")

        self.template = self.template.replace("###HIERARCHY_DISPLAY###", hierarchy_representation)

        return self.template

    def get_hierarchy_template(self):
        html_template = """
        <!DOCTYPE html>
        <html>
        <link rel="stylesheet" href="###JS_LOCATION_TAG###/themes/default/style.min.css" />

        <div id="jstree">
            ###HIERARCHY_DISPLAY###
        </div>

        <!-- 4 include the jQuery library -->
        <script src="###JS_LOCATION_TAG###/jquery-2.2.3.min.js"></script>
        <!-- 5 include the minified jstree source -->
        <script src="###JS_LOCATION_TAG###/jstree.min.js"></script>
        <script>
        $(function () {
          $('#jstree').jstree();
        });
        </script>
        </html>
        """

        return html_template

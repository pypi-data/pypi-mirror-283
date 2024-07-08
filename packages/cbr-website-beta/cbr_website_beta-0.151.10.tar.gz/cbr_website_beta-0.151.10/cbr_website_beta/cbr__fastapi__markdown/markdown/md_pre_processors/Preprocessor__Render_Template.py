import re

from flask                  import render_template
from markdown.preprocessors import Preprocessor


class Preprocessor__Render_Template(Preprocessor):
    RE = re.compile(r'{{render_template\("([^"]+)"\)}}')

    def __init__(self, md):
        super().__init__(md)

    def run(self, lines):
        new_lines = []
        try:
            for line in lines:
                m = self.RE.search(line)
                if m:
                    template_path = m.group(1)
                    rendered_template = render_template(template_path)
                    new_lines.append(rendered_template)
                else:
                    new_lines.append(line)
            return new_lines
        except Exception as error:
            error_message = f'Error in Preprocessor__Render_Template: {error}'
            new_lines.append(error_message)
        return new_lines
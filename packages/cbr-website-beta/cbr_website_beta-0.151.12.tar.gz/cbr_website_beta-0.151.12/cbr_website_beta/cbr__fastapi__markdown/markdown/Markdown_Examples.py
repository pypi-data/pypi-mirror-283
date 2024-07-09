from osbot_utils.base_classes.Type_Safe import Type_Safe


class Markdown_Examples:

    def all_examples(self):

        return dict(markdown        = self.markdown(),
                    render_template = {'simple': RENDER_TEMPLATE},
                    mermaid         = {'graph': '```mermaid\ngraph TD;\n    A-->B;\n    A-->C;\n    B-->D;\n    C-->D;\n```\n'})

    def markdown(self):
        hello_world = "hello world"
        headers     = '## Headers\n\n# Header 1\n## Header 2\n### Header 3\n#### Header 4\n##### Header 5\n###### Header 6\n\n'
        links       = '## Links\n\n[Google](https://www.google.com)\n\n'
        return dict(hello_world = hello_world,
                    headers     = headers    ,
                    links       = links      )

RENDER_TEMPLATE = """'''
This is a Markdown content.

{{render_template("includes/sidebar.html")}}    
'''"""


markdown_examples = Markdown_Examples()
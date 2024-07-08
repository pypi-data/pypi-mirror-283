from markdown import Extension

from cbr_website_beta.cbr__fastapi__markdown.markdown.md_pre_processors.Preprocessor__Render_Template import \
    Preprocessor__Render_Template


class Extension__Render_Template(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(Preprocessor__Render_Template(md), 'flask_template', 175)

import frontmatter
from markdown import Markdown

from cbr_website_beta.cbr__fastapi__markdown.markdown.md_extensions.Extension__Mermaid import Extension__Mermaid
from cbr_website_beta.cbr__fastapi__markdown.markdown.md_extensions.Extension__Render_Template import \
    Extension__Render_Template
from cbr_website_beta.cbr__fastapi__markdown.markdown.md_extensions.Extension__Video import Extension__Video
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.decorators.methods.cache_on_self import cache_on_self


class Markdown_Parser(Type_Safe):

    @cache_on_self
    def markdown(self):
        return Markdown(extensions=self.extensions())

    def extensions(self):
        return [Extension__Mermaid          (),
                Extension__Render_Template  (),
                Extension__Video            ()]

    def markdown_to_html(self, markdown_text):
        return self.markdown().convert(markdown_text)

    def content_to_html(self, content):
        _, markdown = frontmatter.parse(content)
        return  self.markdown_to_html(markdown)

markdown_parser = Markdown_Parser()
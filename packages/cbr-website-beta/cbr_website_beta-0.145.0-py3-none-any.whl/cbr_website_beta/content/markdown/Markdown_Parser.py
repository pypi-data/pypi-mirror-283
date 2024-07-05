import frontmatter
from markdown import Markdown

from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.decorators.methods.cache_on_self import cache_on_self


class Markdown_Parser(Type_Safe):

    @cache_on_self
    def markdown(self):
        return Markdown()

    def markdown_to_html(self, markdown_text):
        return self.markdown().convert(markdown_text)

    def content_to_html(self, content):
        _, markdown = frontmatter.parse(content)
        return  self.markdown_to_html(markdown)

markdown_parser = Markdown_Parser()
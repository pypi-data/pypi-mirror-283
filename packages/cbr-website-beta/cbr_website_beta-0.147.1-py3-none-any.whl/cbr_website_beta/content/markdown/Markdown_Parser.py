import frontmatter
from markdown import Markdown

from cbr_website_beta.content.markdown.Markdown__Ex__Mermaid import Markdown__Ex__Mermaid
from cbr_website_beta.content.markdown.video_extension import VideoExtension
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.decorators.methods.cache_on_self import cache_on_self


class Markdown_Parser(Type_Safe):

    @cache_on_self
    def markdown(self):
        return Markdown(extensions=self.extensions())

    def extensions(self):
        return [Markdown__Ex__Mermaid(), VideoExtension()]

    def markdown_to_html(self, markdown_text):
        return self.markdown().convert(markdown_text)

    def content_to_html(self, content):
        _, markdown = frontmatter.parse(content)
        return  self.markdown_to_html(markdown)

markdown_parser = Markdown_Parser()
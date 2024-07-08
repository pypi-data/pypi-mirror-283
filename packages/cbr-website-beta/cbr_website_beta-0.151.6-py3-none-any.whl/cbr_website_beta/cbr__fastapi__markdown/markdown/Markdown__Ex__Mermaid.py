import re
import xml.etree.ElementTree as etree

from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from osbot_utils.base_classes.Type_Safe import Type_Safe

MERMAID_BLOCK_RE = re.compile(r'^\s*```mermaid\s*\n(.*?)\n\s*```\s*$', re.DOTALL | re.MULTILINE)

class Markdown__Ex__Mermaid(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(Mermaid_Block_Processor(md.parser), 'mermaid', 175)

    def __repr__(self):
        return f'Markdown__Ex__Mermaid'

class Mermaid_Block_Processor(BlockProcessor):

    def test(self, parent, block):
        return bool(MERMAID_BLOCK_RE.search(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = MERMAID_BLOCK_RE.search(block)
        if m:
            code = m.group(1)
            pre = etree.SubElement(parent, 'pre')
            pre.set('class', 'mermaid')
            pre.text = code
            script = etree.SubElement(parent, 'script')
            script.set('type', 'module')
            script.text = """
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.esm.min.mjs';
                mermaid.initialize({ startOnLoad: true });
            """


def makeExtension(**kwargs):
    return Markdown__Ex__Mermaid(**kwargs)
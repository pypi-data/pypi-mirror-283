import re
import xml.etree.ElementTree as etree


from markdown.blockprocessors import BlockProcessor
from osbot_utils.base_classes.Type_Safe import Type_Safe

MERMAID_BLOCK_RE = re.compile(r'^\s*```mermaid\s*\n(.*?)\n\s*```\s*$', re.DOTALL | re.MULTILINE)


class Markdown__Ex__Mermaid(BlockProcessor):
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
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({ startOnLoad: true });
            """

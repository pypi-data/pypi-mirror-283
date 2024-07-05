from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from xml.etree.ElementTree import Element, SubElement
import re

VIDEO_RE = r'\[video:(.*?)(?:\|(.*?))?\]'
DEFAULT_VIDEO_WIDTH = '500'

class VideoExtension(Extension):
    def extendMarkdown(self, md):
        video_pattern = VideoPattern(VIDEO_RE, self.getConfigs())
        md.inlinePatterns.register(video_pattern, 'video', 175)

class VideoPattern(Pattern):
    def handleMatch(self, m):
        video_url = m.group(2).strip()
        video_width = m.group(3).strip() if m.group(3) else DEFAULT_VIDEO_WIDTH
        video = Element('video')
        video.set('controls', '')
        if video_width:
            video.set('width', video_width)
        source = SubElement(video, 'source')
        source.set('src', video_url)
        source.set('type', 'video/mp4')
        return video

def makeExtension(**kwargs):
    return VideoExtension(**kwargs)

# why use PartialGithubFlavoredMarkdownExtension istead of GithubFlavoredMarkdownExtension?
# the latter transforms all line-breaks to <br> tags, https://github.com/Python-Markdown/markdown/issues/1302

from mdx_gfm import PartialGithubFlavoredMarkdownExtension
from gfm import AutolinkExtension, AutomailExtension, TaskListExtension

ext = [
  'markdown.extensions.extra',
  'markdown.extensions.codehilite',
  PartialGithubFlavoredMarkdownExtension(),
  AutolinkExtension(), 
  AutomailExtension(), 
  TaskListExtension(), 
  ]

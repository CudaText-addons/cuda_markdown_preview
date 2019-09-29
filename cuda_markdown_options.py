from mdx_gfm import GithubFlavoredMarkdownExtension
from gfm import AutolinkExtension, AutomailExtension, TaskListExtension

ext = [
  'markdown.extensions.extra',
  'markdown.extensions.codehilite',
  GithubFlavoredMarkdownExtension(),
  AutolinkExtension(), 
  AutomailExtension(), 
  TaskListExtension(), 
  ]

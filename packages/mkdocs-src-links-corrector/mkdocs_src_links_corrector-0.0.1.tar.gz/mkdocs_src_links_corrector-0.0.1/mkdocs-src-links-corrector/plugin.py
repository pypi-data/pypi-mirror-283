import logging
import os
import pathlib
import re
from urllib.parse import quote
from collections import defaultdict

from mkdocs.plugins import BasePlugin

LOG = logging.getLogger("mkdocs.plugins." + __name__)

# Regular expression to match <img> tags with src starting with ./
IMG_SRC_RE = r'(<img\s+[^>]*src=")(\./[^"]+)(")'

class ImgSrcReplacer:
    def __init__(self, base_docs_dir, abs_page_path, filename_to_abs_path):
        self.base_docs_dir = base_docs_dir
        self.abs_page_path = abs_page_path
        self.filename_to_abs_path = filename_to_abs_path

    def __call__(self, match):
        # Extract the parts of the match
        before_src = match.group(1)
        src_value = match.group(2)
        after_src = match.group(3)

        # Replace the initial ./ with ../
        new_src_value = src_value.replace("./", "../", 1)

        # Construct the new <img> tag with the updated src
        return f'{before_src}{new_src_value}{after_src}'


class ImgSrcPlugin(BasePlugin):
    def __init__(self):
        self.filename_to_abs_path = None

    def on_page_markdown(self, markdown, page, config, files, **kwargs):
        # Initializes the filename lookup dict if it hasn't already been initialized
        if self.filename_to_abs_path is None:
            self.init_filename_to_abs_path(files)

        # Getting the root location of markdown source files
        base_docs_dir = config["docs_dir"]

        # Getting the page path that we are linking from
        abs_page_path = page.file.abs_src_path

        # Look for <img> tag matches and replace
        markdown = re.sub(
            IMG_SRC_RE,
            ImgSrcReplacer(base_docs_dir, abs_page_path, self.filename_to_abs_path),
            markdown,
        )

        return markdown

    def init_filename_to_abs_path(self, files):
        self.filename_to_abs_path = defaultdict(list)
        for file_ in files:
            filename = os.path.basename(file_.abs_src_path)
            self.filename_to_abs_path[filename].append(file_.abs_src_path)

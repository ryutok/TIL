#!/usr/bin/env python3

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

# Parameters
SRC_DIR = Path(__file__).parent
ROOT_DIR = SRC_DIR / '../'  # Directory the markdown file stored
DUMP_PATH = SRC_DIR / 'dump.json'  # File path of dump file
TEMP_PATH = SRC_DIR / 'README_templ.md'  # File path of README template
OUT_PATH = ROOT_DIR / 'README.md'  # File path of output
EXCEPTION = ['.git', '.mk_index', 'README.md']  # Except files and directories


class FileInfo():
    def __init__(self, path: Path):
        if not path.is_file():
            raise IOError('No such file: {}'.format(path))

        self.path = path
        h1, h2 = self._get_header()
        if len(h1) == 1:
            title = h1[0]
        else:
            title = self.path.stem
        self.title = title

    def _get_header(self) -> Tuple[List[str], List[str]]:
        h1 = []
        h2 = []
        with self.path.open() as f:
            for line in f:
                if re.match(r'^(#{1})(?!#)', line):
                    head = re.sub(r'^(#+)', '', line)
                    h1.append(head.strip())
                if re.match(r'^(#{2})(?!#)', line):
                    head = re.sub(r'^(#+)', '', line)
                    h2.append(head.strip())
        return h1, h2

    def dump(self) -> Dict[str, str]:
        dump_dict: Dict[str, str] = dict()
        dump_dict['path'] = str(self.path.relative_to(ROOT_DIR))
        dump_dict['title'] = self.title
        return dump_dict


class DirInfo():
    def __init__(self, dir_path: Path):
        if not dir_path.is_dir():
            raise IOError('No such directory: {}'.format(dir_path))

        self.path = dir_path
        self._set_info()

    def _set_info(self):
        dirs = []
        files = []
        for item in self.path.glob('*'):
            if item.name in EXCEPTION:
                pass
            elif item.is_dir():
                dirs.append(item)
            elif item.is_file() and item.suffix == '.md':
                files.append(item)
        dirs.sort()
        files.sort()

        self.files = [FileInfo(item) for item in files]
        self.directories = [DirInfo(item) for item in dirs]

    def dump(self) -> Dict[str, Union[str, List[Any]]]:
        dump_dict: Dict[str, Union[str, List[Any]]] = dict()
        dump_dict['path'] = str(self.path.relative_to(ROOT_DIR))
        dump_dict['files'] = [item.dump() for item in self.files]
        dump_dict['directories'] = [item.dump() for item in self.directories]
        return dump_dict

    def get_categories(self, n: int = 0) -> List[str]:
        lines: List[str] = []
        for item in self.directories:
            name = item.path.name
            lines.append('    '*n + '- [' + name + '](#' + name.lower() + ')')
            lines += item.get_categories(n+1)
        return lines

    def get_toc(self, n: int = 0) -> List[str]:
        lines: List[str] = []
        for item in self.files:
            path = str(item.path.relative_to(OUT_PATH.parent))
            lines.append('- [' + item.title + '](' + path + ')')
        for item in self.directories:
            lines.append('')
            lines.append('###' + '#'*n + ' ' + item.path.name)
            lines.append('')
            lines += item.get_toc(n+1)
        if lines[0] == '':
            lines.pop(0)
        return lines


def make_index(contents: DirInfo):
    """
    Insert categories list and TOC in README file.
    """

    lines: List[str] = []
    categories = contents.get_categories()
    toc = contents.get_toc()
    with open(TEMP_PATH) as f:
        for line in f:
            line = line.rstrip()
            if re.match(r'^(<!--#md_indexer categories)(.*)(-->)', line):
                lines += categories
            elif re.match(r'^(<!--#md_indexer toc)(.*)(-->)', line):
                lines += toc
            else:
                lines.append(line)
    with open(OUT_PATH, 'w') as f:
        f.write('\n'.join(lines))


def main():
    # Get directory informations
    info = {
        'contents_path': str(ROOT_DIR.resolve()),
        'updated_at': datetime.now().isoformat(),
    }
    contents = DirInfo(ROOT_DIR)
    info['contents'] = contents.dump()

    # Dump informations
    if not DUMP_PATH.parent.exists():
        DUMP_PATH.parent.mkdir()
    with open(DUMP_PATH, 'w') as f:
        json.dump(info, f, indent=4)

    # Make README file
    make_index(contents)


if __name__ == '__main__':
    main()

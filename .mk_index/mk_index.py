#!/usr/bin/env python3

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

SRC_DIR = Path(__file__).parent
MD_DIR = SRC_DIR / '../'  # Directory the markdown file stored
DUMP_PATH = SRC_DIR / 'dump.json'  # File path of dump file
TEMP_PATH = SRC_DIR / 'README_templ.md'  # File path of README template
OUT_PATH = MD_DIR / 'README.md'  # File path of output
EXCEPTION = ['.git', '.mk_index', 'README.md']  # Except files and directories


def _scan_dir(dir_path: Path, excpt: List[str])\
        -> Tuple[List[Path], List[Path]]:
    """
    Get directory and file list in the specified directory.
    """

    if not dir_path.is_dir():
        raise IOError('No such directory: {}'.format(dir_path))

    dirs = []
    files = []
    for item in dir_path.glob('*'):
        if item.name in excpt:
            pass
        elif item.is_dir():
            dirs.append(item)
        elif item.is_file() and item.suffix == '.md':
            files.append(item)

    dirs.sort()
    files.sort()
    return dirs, files


def _scan_file(file_path: Path) -> Tuple[List[str], List[str]]:
    """
    Get the first and second heads of the specified markdown file.
    """

    if not file_path.is_file():
        raise IOError('No such file: {}'.format(file_path))

    h1 = []
    h2 = []
    with file_path.open() as f:
        for line in f:
            if re.match(r'^(#{1})(?!#)', line):
                head = re.sub(r'^(#+)', '', line)
                h1.append(head.strip())
            if re.match(r'^(#{2})(?!#)', line):
                head = re.sub(r'^(#+)', '', line)
                h2.append(head.strip())

    return h1, h2


def _get_dir_info(dirs: List[str], parent_dir: Path) -> List[Dict[str, str]]:
    """
    Scan files and directories recursively.
    """

    dir_info = []
    for suffix in dirs:
        dump = dict()
        dump['path'] = suffix
        dir_path = parent_dir / suffix
        sub_dirs, sub_files = _scan_dir(dir_path, EXCEPTION)
        file_info = []
        for file_path in sub_files:
            h1, h2 = _scan_file(file_path)
            if len(h1) == 1:
                title = h1[0]
            else:
                title = file_path.stem
            file_info.append(
                    {'path': str(file_path.relative_to(dir_path)),
                     'title': title,
                     }
            )
        dump['files'] = file_info
        sub_dirs = [str(path.relative_to(dir_path)) for path in sub_dirs]
        dump['directories'] = _get_dir_info(sub_dirs, dir_path)
        dir_info.append(dump)
    return dir_info


def get_info(contents_dir: Path, store_path: Path) -> Dict[str, str]:
    """
    Scan directory and dump and restore the data.
    """

    # Check contents and its updated time
    if not contents_dir.is_dir():
        raise IOError('No such directory: {}'.format(contents_dir))
    # mtimes = [item.stat().st_mtime for item in contents_dir.glob('**')]
    # update_time = datetime.fromtimestamp(max(mtimes))

    # # Restore dumped file
    # if store_path.is_file():
    #     with open(store_path) as f:
    #         info = json.load(f)
    #     dump_time = datetime.fromisoformat(info.get('updated_at'))
    #     if dump_time > update_time:
    #         return info

    # Get directory informations
    info = {
        'contents_path': str(contents_dir.resolve()),
        'updated_at': datetime.now().isoformat(),
        'stored_in': str(store_path.resolve())
    }
    contents = _get_dir_info(['.'], contents_dir)
    info['contents'] = contents[0]

    # Dump informations
    if not store_path.parent.exists():
        store_path.parent.mkdir()
    with open(store_path, 'w') as f:
        json.dump(info, f, indent=4)

    return info


def _make_dir_list(contents: Dict[str, str], n: int = 0) -> str:
    """
    Return directories list in markdown format.
    """

    lines = []
    for item in contents.get('directories'):
        path = item.get('path')
        lines.append('    '*n + '- [' + path + '](#' + path + ')')
        lines += _make_dir_list(item, n+1)

    lines = '\n'.join(lines)
    return lines


def _make_toc(contents: Dict[str, str], root_path: Path,
              cont_path: Path = None, n: int = 0) -> str:
    """
    Return table of contents in markdown format.
    """

    if cont_path is None:
        cont_path = root_path
    lines = []
    for item in contents.get('files'):
        item_path = cont_path / item.get('path')
        lines.append('- [' + item.get('title') + ']('
                     + str(item_path.relative_to(root_path)) + ')')
    for item in contents.get('directories'):
        lines.append('\n###' + '#'*n + ' ' + item.get('path') + '\n')
        item_path = cont_path / item.get('path')
        lines.append(_make_toc(item, root_path, item_path, n+1))

    line = '\n'.join(lines)
    return line


def make_index(info: Dict[str, str], out_path: Path,
               temp_path: Path) -> None:
    """
    Insert directory list and TOC in README file.
    """

    lines = ''
    contents = info.get('contents')
    dirs = _make_dir_list(contents)
    toc = _make_toc(contents, out_path)
    with open(temp_path) as f:
        for line in f:
            if re.match(r'^(<!--#md_indexer directories)(.*)(-->)', line):
                lines += dirs + '\n'
            elif re.match(r'^(<!--#md_indexer toc)(.*)(-->)', line):
                lines += toc + '\n'
            else:
                lines += line
    with open(out_path, 'w') as f:
        for line in lines:
            f.write(line)


def main():
    info = get_info(MD_DIR, DUMP_PATH)
    make_index(info, OUT_PATH, TEMP_PATH)


if __name__ == '__main__':
    main()

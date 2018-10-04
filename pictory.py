import mimetypes as mimes
import os
import re
import shutil
import sys
from collections import defaultdict
from typing import Callable

import pendulum

try:
    path = sys.argv[1]
except IndexError:
    path = '.'

base_output_path = os.path.join(path, __file__[:-3])

files = {
    os.path.join(root, _file)
    for root, dirs, files in os.walk(path)
    for _file in files
}

def _is_ext(_type) -> Callable:
    def guess(_file) -> bool:
        g, _ = mimes.guess_type(_file)
        if not g:
            return False
        return g.startswith(_type)
    return guess
is_img, is_video = _is_ext('image'), _is_ext('video')

pictures = (_file for _file in files if is_img(_file))
videos = (_file for _file in files if is_video(_file))


def structured_collection(collection) -> tuple:
    structured = defaultdict(lambda: defaultdict(list))
    unknowns = set()
    for item in collection:
        match = re.match(r'.*((19|20)\d{6}_(\d{2})\d{4}).*', item)
        if not match:
            unknowns.add(item)
            continue

        datetime = match.group(1)
        hour = match.group(3)
        # ugly hour >= 24 hack
        if hour == '24':
            datetime = f'{datetime[:9]}00{datetime[11:15]}'

        clock = pendulum.from_format(datetime, 'YYYYMMDD_HHmmss')
        # ugly hour >= 24 hack
        if hour == '24':
            clock = clock.add(days=1)

        year, month, stamp = clock.format('YYYY MMMM DD_HHmm').split()
        structured[year][month].append((item, stamp))
    return (structured, unknowns)


def copyerino(collection_name, structured_collection, unknowns) -> None:
    for year, months in structured_collection.items():
        for month, items in months.items():
            for source, destination in items:
                source_ext = source.split('.')[-1]
                path = os.path.join(
                    base_output_path, collection_name, year, month)

                if not os.path.exists(path):
                    os.makedirs(path)
                shutil.copy(source, os.path.join(path, f'{destination}.{source_ext}'))
    
    if not unknowns:
        return 

    path = os.path.join(base_output_path, collection_name, 'unknowns')
    if not os.path.exists(path):
        os.makedirs(path)
    for unknown in unknowns:
        shutil.copy(unknown, path)


copyerino('images', *structured_collection(pictures))
copyerino('videos', *structured_collection(videos))
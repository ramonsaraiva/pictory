import mimetypes as mimes
import os
import re
import shutil
import sys
from collections import defaultdict

import pendulum


BASE_OUTPUT_PATH = __file__[:-3]

try:
    path = sys.argv[1]
except IndexError:
    path = '.'

files = {
    os.path.join(root, _file)
    for root, dirs, files in os.walk(path)
    for _file in files
}

_is_ext = lambda _type: lambda _file: mimes.guess_type(_file)[0].startswith(_type)
is_img, is_video = _is_ext('image'), _is_ext('video')

pictures = (_file for _file in files if is_img(_file))
videos = (_file for _file in files if is_video(_file))


def structured_collection(collection) -> tuple:
    structured = defaultdict(lambda: defaultdict(list))
    unknowns = set()
    for item in collection:
        match = re.match(r'.*((19|20)\d{6}_\d{6}).*', item)
        if not match:
            unknowns.add(item)
            continue
        clock = pendulum.from_format(match.group(1), 'YYYYMMDD_HHmmss')
        year, month, stamp  = clock.format('YYYY MMMM DD_HHmm').split()
        structured[year][month].append((item, stamp))
    return (structured, unknowns)


def copyerino(collection_name, structured_collection, unknowns):
    for year, months in structured_collection.items():
        for month, items in months.items():
            for source, destination in items:
                source_ext = source.split('.')[-1]
                path = os.path.join(
                    BASE_OUTPUT_PATH, collection_name, year, month)

                if not os.path.exists(path):
                    os.makedirs(path)
                shutil.copy(source, os.path.join(path, f'{destination}.{source_ext}'))
    
    if not unknowns:
        return 

    path = os.path.join(BASE_OUTPUT_PATH, collection_name, 'unknowns')
    if not os.path.exists(path):
        os.makedirs(path)
    for unknown in unknowns:
        shutil.copy(unknown, path)


copyerino('images', *structured_collection(pictures))
copyerino('videos', *structured_collection(videos))
import mimetypes as mimes
import os
import re
import shutil
import sys
from collections import defaultdict
from typing import (
    Callable,
    Tuple,
)

import pendulum


def main():
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

    pictures = (_file for _file in files if is_img(_file))
    videos = (_file for _file in files if is_video(_file))

    copyerino(base_output_path, 'images', *structured_collection(pictures))
    copyerino(base_output_path, 'videos', *structured_collection(videos))


def _is_ext(_type) -> Callable:
    def guess(_file) -> bool:
        g, _ = mimes.guess_type(_file)
        if not g:
            return False
        return g.startswith(_type)
    return guess
is_img, is_video = _is_ext('image'), _is_ext('video')


def structured_collection(collection) -> Tuple[dict, set]:
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

        year, month = clock.format('YYYY MMMM').split()
        structured[year][month].append(item)
    return (structured, unknowns)


def copyerino(base_output_path, collection_name, collection, unknowns) -> None:
    def files():
        for year, months in collection.items():
            for month, items in months.items():
                for file_path in items:
                    yield (year, month, file_path)

    collection_output_path = os.path.join(
        base_output_path, collection_name)

    for year, month, file_path in files():
        output_path = os.path.join(collection_output_path, year, month)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        output_file = os.path.basename(file_path)
        shutil.copy(file_path, os.path.join(output_path, output_file))
        
    if unknowns:
        unknowns_path = os.path.join(collection_output_path, 'unknowns')
        if not os.path.exists(unknowns_path):
            os.makedirs(path)
        for unknown in unknowns:
            shutil.copy(unknown, path)


if __name__ == '__main__':
    main()
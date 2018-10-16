import argparse
from datetime import datetime
import mimetypes as mimes
import os
import re
import shutil
from collections import defaultdict
from typing import (
    Callable,
    Tuple,
)

count_int = 0


def over_strategy(src, des_path, filename)-> None:
    shutil.move(src, os.path.join(des_path, filename))


def pref_strategy(src, des_path, filename)-> None:
    global count_int
    count_int += 1
    new_filename = str(count_int) + '_' + filename
    shutil.copy(src, os.path.join(des_path, new_filename))


def suff_strategy(src, des_path, filename) -> None:
    global count_int
    count_int += 1
    new_filename = filename.split('.')[0] + '_' + str(count_int) + '.' + filename.split('.')[1]
    shutil.copy(src, os.path.join(des_path, new_filename))


duplicates_strategies = {'skip': lambda: None,
                         'over': over_strategy,
                         'pref': pref_strategy,
                         'suff': suff_strategy}


def main(path, duplicate) -> None:
    base_output_path = os.path.join(path, 'pictory')

    files = {
        os.path.join(root, _file)
        for root, dirs, files in os.walk(path)
        for _file in files
    }

    pictures = (_file for _file in files if is_img(_file))
    videos = (_file for _file in files if is_video(_file))

    copyerino(base_output_path, 'images', duplicate, *structured_collection(pictures))
    copyerino(base_output_path, 'videos', duplicate, *structured_collection(videos))


def _is_ext(_type) -> Callable:
    def guess(_file) -> bool:
        g, _ = mimes.guess_type(_file)
        return g.startswith(_type) if g else False
    return guess
is_img, is_video = _is_ext('image'), _is_ext('video')


def structured_collection(collection) -> Tuple[dict, set]:
    structured = defaultdict(lambda: defaultdict(list))
    unknowns = set()
    for item in collection:
        match = re.match(r'.*(((19|20)\d{6})_\d{6}).*', item)
        if not match:
            unknowns.add(item)
            continue

        date = datetime.strptime(match.group(2), '%Y%m%d')
        year, written_month = date.strftime('%Y %B').split()
        structured[year][written_month].append(item)
    return (structured, unknowns)


def copyerino(base_output_path, collection_name, duplicates, collection, unknowns) -> None:
    def files():
        for year, months in collection.items():
            global count_int
            count_int = 0
            for month, items in months.items():
                count_int = 0
                for file_path in items:
                    yield (year, month, file_path)

    collection_output_path = os.path.join(
        base_output_path, collection_name)

    for year, month, file_path in files():
        output_path = os.path.join(collection_output_path, year, month)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_file = os.path.basename(file_path)
        try:
            shutil.copy(file_path, os.path.join(output_path, output_file))
        except shutil.SameFileError:
            duplicates_strategies[duplicates](file_path, output_path, output_file)

    if unknowns:
        unknowns_path = os.path.join(collection_output_path, 'unknowns')
        if not os.path.exists(unknowns_path):
            os.makedirs(path)
        for unknown in unknowns:
            shutil.copy(unknown, path)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Simple tool to organize pictures and videos in lickable directories')
    parser.add_argument('path', metavar='path', type=str,
                        help='path of directory to organize')

    parser.add_argument('--duplicates', metavar='duplicates', type=str, default='skip',
                        choices=list(duplicates_strategies.keys()),
                        help='action to take in case of collision: {}'.format(list(duplicates_strategies.keys())))

    args = parser.parse_args()
    main(args.path, args.duplicates)

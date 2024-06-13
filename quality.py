#!/usr/bin/python3

import pathlib
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from typing import Dict, List, Tuple

from tqdm import tqdm

from image import Image


def low_quality(image: Image) -> bool:
    known = load_dimensions()
    width, height = known[image.id]
    return width <= 700


def record_all_dimensions(images: List[Image]) -> None:
    known = load_dimensions()

    missing = [img for img in images if img.id not in known]
    if not missing:
        return

    with open(csv_path, 'a') as fd:
        with ThreadPoolExecutor() as executor:
            futures = []
            for img in missing:
                futures.append(executor.submit(dimensions, img))

            for result in tqdm(as_completed(futures), total=len(missing), desc='Measuring'):
                print(result.result(), file=fd)


@lru_cache(None)
def load_dimensions() -> Dict[str, Tuple[int, int]]:
    result: Dict[str, Tuple[int, int]] = {}

    with open(csv_path) as fd:
        for line in fd:
            img, width, height = line.strip().split(',')
            result[img] = (int(width), int(height))

    return result


# PRIVATE

csv_path = str(pathlib.Path(__file__).parent.absolute()) + '/data/quality.csv'


def dimensions(image: Image) -> str:
    result = subprocess.check_output(['identify', '-format', '%w,%h', image.path])
    result = result.decode('utf-8').strip()
    return f'{image.id},{result}'

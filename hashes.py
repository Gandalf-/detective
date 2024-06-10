#!/usr/bin/python3

import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from typing import List, Set

from tqdm import tqdm

from image import Image

web_root = os.path.expanduser('~/working/object-publish/detective')


def create_webp(images: List[Image]) -> None:
    smalls = existing_smalls()
    larges = existing_larges()
    total_tasks = sum(img.id not in smalls for img in images) + sum(
        img.id not in larges for img in images
    )

    with ThreadPoolExecutor() as executor:
        futures = []
        for img in images:
            if img.id not in smalls:
                futures.append(executor.submit(create_thumbnail, img))
            if img.id not in larges:
                futures.append(executor.submit(create_fullsize, img))

        # Iterate through completed futures and update the progress bar
        for _ in tqdm(as_completed(futures), total=total_tasks, desc='Optimizing images'):
            pass


# PRIVATE


def convert(opts: List[str]) -> None:
    defaults = ['convert', '-strip', '-auto-orient']
    cmd = defaults + opts
    subprocess.run(cmd)


def create_thumbnail(image: Image) -> None:
    output = os.path.join(web_root, 'small', f'{image.id}.webp')
    assert not os.path.exists(output)
    convert(
        [
            '-quality',
            '70%',
            image.path,
            output,
        ]
    )


def create_fullsize(image: Image) -> None:
    output = os.path.join(web_root, 'large', f'{image.id}.webp')
    assert not os.path.exists(output)
    convert(
        [
            '-quality',
            '35',
            image.path,
            output,
        ]
    )


@lru_cache(None)
def existing_smalls() -> Set[str]:
    return {c.strip('.webp') for c in os.listdir(os.path.join(web_root, 'small'))}


@lru_cache(None)
def existing_larges() -> Set[str]:
    return {c.strip('.webp') for c in os.listdir(os.path.join(web_root, 'large'))}

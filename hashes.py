#!/usr/bin/python3

import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from typing import Set

from image import Image, load_everything

web_root = os.path.expanduser('~/working/object-publish/detective')


def quality_hashes(image: Image) -> Set[str]:
    smalls = existing_smalls()
    larges = existing_larges()


def create_webp() -> None:
    images = load_everything()
    smalls = existing_smalls()
    larges = existing_larges()

    with ThreadPoolExecutor() as executor:
        for img in images:
            if img.id not in smalls:
                executor.submit(create_thumbnail, img)
            if img.id not in larges:
                executor.submit(create_fullsize, img)


# PRIVATE


def create_thumbnail(image: Image) -> None:
    output = os.path.join(web_root, 'small', f'{image.id}.webp')
    assert not os.path.exists(output)
    cmd = (
        'convert',
        '-strip',
        '-auto-orient',
        '-interlace',
        'plane',
        '-resize',
        '350',
        '-quality',
        '60%',
        image.path,
        output,
    )
    subprocess.run(cmd)
    print(f'created {output}', file=sys.stderr)


def create_fullsize(image: Image) -> None:
    output = os.path.join(web_root, 'large', f'{image.id}.webp')
    assert not os.path.exists(output)
    cmd = (
        'convert',
        '-strip',
        '-auto-orient',
        '-quality',
        '35',
        image.path,
        output,
    )
    subprocess.run(cmd)
    print(f'created {output}', file=sys.stderr)


@lru_cache(None)
def existing_smalls() -> Set[str]:
    return {c.strip('.webp') for c in os.listdir(os.path.join(web_root, 'small'))}


@lru_cache(None)
def existing_larges() -> Set[str]:
    return {c.strip('.webp') for c in os.listdir(os.path.join(web_root, 'large'))}


if __name__ == '__main__':
    create_webp()

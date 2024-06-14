#!/usr/bin/python3

import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from tqdm import tqdm

import config
from image import Image


def create_webp(images: List[Image]) -> None:
    with ThreadPoolExecutor() as executor:
        futures = []
        for img in images:
            futures.append(executor.submit(_create_thumbnail, img))
            futures.append(executor.submit(_create_fullsize, img))

        for _ in tqdm(as_completed(futures), total=len(images) * 2, desc='Optimizing'):
            pass

    desired = {f'{img.id}.webp' for img in images}
    to_remove: List[str] = []

    for root in ('small', 'large'):
        existing = set(os.listdir(os.path.join(config.web_root, root)))
        stale = existing - desired
        for s in stale:
            to_remove.append(os.path.join(config.web_root, root, s))

    if to_remove:
        for s in tqdm(to_remove, total=len(to_remove), desc='Cleaning  '):
            os.remove(s)


# PRIVATE


def _convert(opts: List[str]) -> None:
    defaults = ['convert', '-strip', '-auto-orient']
    cmd = defaults + opts
    subprocess.run(cmd)


def _create_thumbnail(image: Image) -> None:
    output = os.path.join(config.web_root, 'small', f'{image.id}.webp')
    if os.path.exists(output):
        return
    _convert(
        [
            '-quality',
            '70%',
            '-resize',
            '320000@',
            image.path,
            output,
        ]
    )


def _create_fullsize(image: Image) -> None:
    output = os.path.join(config.web_root, 'large', f'{image.id}.webp')
    if os.path.exists(output):
        return
    _convert(
        [
            '-quality',
            '35',
            image.path,
            output,
        ]
    )

#!/usr/bin/python3

from functools import lru_cache
from typing import Any, Dict, List, Optional

import yaml

from util import config


@lru_cache(None)
def load_taxonomy() -> Dict[str, str]:
    yml_path = f'{config.src_root}/data/taxonomy.yml'

    with open(yml_path) as fd:
        data = yaml.safe_load(fd)

    return _invert_mapping(data)


# PRIVATE


def _invert_mapping(mapping: Any) -> Dict[str, str]:
    result: Dict[str, str] = {}

    def inner(
        tree: Any,
        out: Dict[str, str],
        lineage: Optional[List[str]] = None,
    ) -> None:
        if not lineage:
            lineage = []

        if tree is None:
            out[lineage[-1]] = ' '.join(lineage)
        elif isinstance(tree, str):
            for part in tree.split(', '):
                out[part] = ' '.join(lineage)
        else:
            for key, value in tree.items():
                inner(value, out, lineage + [key])

    inner(mapping, result)
    return result

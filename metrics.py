"""
An interface for other modules to record interesting information that can then
be displayed at the end of gallery.py's execution.
"""

import json
from typing import Any

from config import src_root


class Metrics:
    def __init__(self) -> None:
        self._data: dict[str, Any] = {}
        self._path = f'{src_root}/data/metrics.json'

    def record(self, key: str, value: Any) -> None:
        self._data.setdefault(key, set())
        self._data[key].add(value)

    def counter(self, key: str, n: int = 1) -> None:
        self._data.setdefault(key, 0)
        self._data[key] += n

    def summary(self) -> None:
        if not self._data:
            return

        previous = self._restore()

        print('Metrics...')
        last = []
        for key, value in sorted(self._data.items()):
            if isinstance(value, (set, list)):
                value = sorted(value)
                last.append(f'\t{key}: {value}')
            else:
                prev = previous.get(key, value)
                diff = value - prev
                diff = f'+{diff}' if diff >= 0 else f'{diff}'
                print(f'\t{value}\t{diff}\t{key}')

        print('')
        for line in sorted(last):
            print(line)

        self._persist()

    def _persist(self) -> None:
        data = {}
        for k, v in self._data.items():
            if isinstance(v, int):
                data[k] = v

        with open(self._path, 'w') as fd:
            json.dump(data, fd, sort_keys=True)

    def _restore(self) -> dict[str, Any]:
        try:
            with open(self._path) as fd:
                return json.load(fd)
        except FileNotFoundError:
            return {}


metrics = Metrics()

"""
An interface for other modules to record interesting information that can then
be displayed at the end of gallery.py's execution.
"""

import json
import pathlib
from typing import Any


class Metrics:
    def __init__(self) -> None:
        self.data: dict[str, Any] = {}

    def record(self, key: str, value: Any) -> None:
        self.data.setdefault(key, set())
        self.data[key].add(value)

    def counter(self, key: str, n: int = 1) -> None:
        self.data.setdefault(key, 0)
        self.data[key] += n

    def summary(self) -> None:
        if not self.data:
            return

        previous = self._restore()

        print('Metrics...')
        last = []
        for key, value in sorted(self.data.items()):
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
        for k, v in self.data.items():
            if isinstance(v, int):
                data[k] = v

        with open(persist_path, 'w') as fd:
            json.dump(data, fd)

    def _restore(self) -> dict[str, Any]:
        try:
            with open(persist_path) as fd:
                return json.load(fd)
        except FileNotFoundError:
            return {}


persist_path = str(pathlib.Path(__file__).parent.absolute()) + '/data/metrics.json'

metrics = Metrics()

#!/usr/bin/python3

import os
from typing import List, Tuple

from hashes import web_root
from species import ImageTree, build_image_tree
from version import VersionedResource

ThumbsTable = List[List[str]]
SimiliarityTable = List[List[int]]
DifficultyTable = List[int]


def table_builder(
    tree: ImageTree,
) -> Tuple[List[str], ThumbsTable, SimiliarityTable, DifficultyTable]:
    names = list(sorted(tree.keys()))

    thumbs: ThumbsTable = [[] for _ in names]
    for i, name in enumerate(names):
        images = tree[name]
        thumbs[i] = [img.id for img in images][:20]

    similarity = _similarity_table(names)
    diffs = _difficulties(names)

    return names, thumbs, similarity, diffs


def writer() -> None:
    tree = build_image_tree()
    ns, ts, ss, ds = table_builder(tree)

    # This saves 100KB of data, ~20% of the total
    ts = str(ts).replace(' ', '')
    ss = str(ss).replace(' ', '')
    ds = str(ds).replace(' ', '')

    with open('data.js', 'w+') as fd:
        print('var main_names =', ns, file=fd)
        print('var main_thumbs =', ts, file=fd)
        print('var main_similarities =', ss, file=fd)
        print('var main_difficulties =', ds, file=fd)

    css = VersionedResource('style.css', web_root)
    game = VersionedResource('game.js', web_root)
    data = VersionedResource('data.js', web_root)

    for vr in [css, game, data]:
        vr.cleanup()
        vr.write()

    with open(os.path.join(web_root, 'index.html'), 'w+') as fd:
        print(_html_builder(css.name, game.name, data.name), file=fd, end='')


# PRIVATE


def _distance(a: str, b: str) -> float:
    return 1


def _difficulties(names: List[str]) -> DifficultyTable:
    return [0 for _ in names]


def _similarity_table(names: List[str]) -> SimiliarityTable:
    """how alike is every name pair"""
    similarity: SimiliarityTable = [[] for _ in names]

    for i, name in enumerate(names):
        for j, other in enumerate(names):
            if i == j:
                similarity[i].append(0)
                continue

            if j > i:
                # should already be done
                continue

            d = _distance(name, other)
            d = int(d * 100)
            similarity[i].append(d)

    return similarity


def _html_builder(css: str, game: str, data: str) -> str:
    """Insert dynamic content into the HTML template"""
    desc = 'Scuba diving picture identification game, identify a picture or choose the image for a name'
    return f"""
<!DOCTYPE html>
<html>
    <head>
        <title>Diving Detective</title>
        <link rel="canonical" href="https://detective.anardil.net/" />
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description"
              content="{desc}">
        <link rel="stylesheet" href="/{css}" />
        <script src="/{data}"></script>
        <script src="/{game}"></script>
        <style>
body {{
    max-width: 1080px;
    margin-left: auto;
    margin-right: auto;
    float: none !important;
}}
        </style>
    </head>

    <body>
        <div class="wrapper">
            <div class="title">
                <a href="/detective/">
                    <h1 class="top switch detective">Detective</h1>
                </a>
                <p class="scientific"></p>
            </div>
            <div id="control">
                <select id="game" onchange="choose_game();">
                    <option value="names">Names</option>
                    <option value="images">Images</option>
                </select>
                <div class="scoring">
                    <h3 id="score"></h3>
                    <h3 id="points"></h3>
                </div>
                <select id="difficulty" onchange="choose_game();">
                    <option value=0>Very Easy</option>
                    <option value=1 selected>Easy</option>
                    <option value=2>Moderate</option>
                    <option value=3>Hard</option>
                    <option value=4>Very Hard</option>
                </select>
            </div>

            <div id="correct_outer">
                <h2 id="correct"></h2>
            </div>

            <div class="grid" id="options">
                <div class="choice" id="option0"> </div>
                <div class="choice" id="option1"> </div>
                <div class="choice" id="option2"> </div>
                <div class="choice" id="option3"> </div>
                <div class="choice" id="option4"> </div>
                <div class="choice" id="option5"> </div>
                <div class="choice" id="option6"> </div>
                <div class="choice" id="option7"> </div>

                <div class="top switch skip" onclick="choose_game();">
                    <h4>Skip</h4>
                </div>
            </div>
        </div>

        <script>
            choose_game();
        </script>
    </body>
</html>
"""


if __name__ == '__main__':
    writer()

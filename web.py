#!/usr/bin/python3

import os
from typing import List, Tuple

from collection import load_images
from metrics import metrics
from optimize import create_webp, web_root
from quality import record_all_dimensions
from species import ImageTree, build_image_tree
from taxonomy import load_taxonomy
from version import VersionedResource

ThumbsTable = List[List[str]]
CreditTable = List[List[int]]
SimiliarityTable = List[List[int]]


def table_builder(
    tree: ImageTree,
) -> Tuple[List[str], ThumbsTable, SimiliarityTable, List[str], CreditTable]:
    names = list(sorted(tree.keys()))

    people = list(sorted({img.credit for images in tree.values() for img in images}))
    thumbs: ThumbsTable = [[] for _ in names]
    credit: CreditTable = [[] for _ in names]

    for i, name in enumerate(names):
        images = tree[name]
        thumbs[i] = [img.id for img in images]

        for img in images:
            who = people.index(img.credit)
            credit[i].append(who)

    similarity = _similarity_table(names)

    return names, thumbs, similarity, people, credit


def writer(tree: ImageTree) -> None:
    ns, ts, ss, ps, cs = table_builder(tree)

    # This saves 100KB of data, ~20% of the total
    ts = str(ts).replace(' ', '')
    ss = str(ss).replace(' ', '')
    cs = str(cs).replace(' ', '')

    with open('/tmp/data.js', 'w+') as fd:
        print('var main_names =', ns, file=fd)
        print('var main_thumbs =', ts, file=fd)
        print('var main_similarities =', ss, file=fd)
        print('var main_people =', ps, file=fd)
        print('var main_credit =', cs, file=fd)

    css = VersionedResource('style.css', web_root)
    game = VersionedResource('game.js', web_root)
    data = VersionedResource('/tmp/data.js', web_root)

    for vr in [css, game, data]:
        vr.cleanup()
        vr.write()

    with open(os.path.join(web_root, 'index.html'), 'w+') as fd:
        print(_html_builder(css.name, game.name, data.name), file=fd, end='')


# PRIVATE


def _distance(a: str, b: str) -> float:
    tree = load_taxonomy()

    at = tree[a].split(' ')
    bt = tree[b].split(' ')

    total = 0
    match = 0

    for x, y in zip(at, bt):
        total += 1
        match += 1 if x == y else 0

    return match / total


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
    desc = 'Test your Reef Check ID expertise with professionally labeled images.'
    return f"""
<!DOCTYPE html>
<html>
    <head>
        <title>Diving Detective</title>
        <link rel="canonical" href="https://detective.anardil.net/" />
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="{desc}">
        <link rel="stylesheet" href="/{css}" />
        <script src="/{data}"></script>
        <script src="/{game}"></script>
    </head>

    <body>
        <div class="wrapper">
            <div class="title">
                <h1 class="top switch detective">Detective</h1>
                <p class="scientific"></p>
            </div>
            <div id="control">
                <select id="game" onchange="choose_game();">
                    <option value="names">Washington</option>
                </select>
                <div class="scoring">
                    <h3 id="score"></h3>
                    <h3 id="points"></h3>
                </div>
                <select id="difficulty" onchange="choose_game();">
                    <option value=0>Very Easy</option>
                    <option value=1>Easy</option>
                    <option value=2>Moderate</option>
                    <option value=3 selected>Hard</option>
                    <option value=4>Very Hard</option>
                </select>
            </div>

            <div id="correct_outer" class="grid correct_name">
                <div class="choice" id="correct"> </div>
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


def main() -> None:
    record_all_dimensions(load_images())

    limit = 20
    tree = build_image_tree()
    metrics.counter('images matched', sum(len(v) for v in tree.values()))

    tree = {k: tree[k][:limit] for k in list(tree)}
    metrics.counter('images used', sum(len(v) for v in tree.values()))
    metrics.counter('species short', sum(1 for v in tree.values() if len(v) < limit))
    metrics.counter('species represented', len(tree))

    writer(tree)

    images = [img for img_list in tree.values() for img in img_list]
    create_webp(images)
    metrics.summary()


if __name__ == '__main__':
    main()

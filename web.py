#!/usr/bin/python3

import os
from typing import Dict, List, Tuple

import collection
import optimize
import quality
import species
import taxonomy
from species import ImageTree
from util import config
from util.metrics import metrics
from util.version import VersionedResource

ThumbsTable = List[List[str]]
CreditTable = List[List[int]]
SimiliarityTable = List[List[int]]


def table_builder(
    tree: ImageTree,
) -> Tuple[List[str], ThumbsTable, List[str], CreditTable]:
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

    return names, thumbs, people, credit


def writer(tree: ImageTree) -> None:
    names, thumbs, people, credit = table_builder(tree)
    thumbs = str(thumbs).replace(' ', '')
    credit = str(credit).replace(' ', '')

    similarity = similarity_table(names)
    similarity = str(similarity).replace(' ', '')

    categories = category_indices(tree)
    categories = str(categories)

    with open('/tmp/data.js', 'w+') as fd:
        print('var g_names =', names, file=fd)
        print('var g_thumbs =', thumbs, file=fd)
        print('var g_similarities =', similarity, file=fd)
        print('var g_people =', people, file=fd)
        print('var g_credit =', credit, file=fd)
        print('var g_categories =', categories, file=fd)

    css = VersionedResource('style.css', config.web_root)
    game = VersionedResource('game.js', config.web_root)
    data = VersionedResource('/tmp/data.js', config.web_root)

    for source in [css, game, data]:
        source.cleanup()
        source.write()

    with open(os.path.join(config.web_root, 'index.html'), 'w+') as fd:
        print(html_builder(css.name, game.name, data.name), file=fd, end='')


def distance(a: str, b: str) -> float:
    tree = taxonomy.load_taxonomy()

    at = tree[a].split(' ')
    bt = tree[b].split(' ')

    total = 0
    match = 0

    for x, y in zip(at, bt):
        total += 1
        match += 1 if x == y else 0

    d = match / total

    if d > 0 and ('Non-' in a + b):
        d = 1.0

    return d


def similarity_table(names: List[str]) -> SimiliarityTable:
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

            d = distance(name, other)
            d = int(d * 100)
            similarity[i].append(d)

    return similarity


def category_indices(tree: ImageTree) -> Dict[str, List[int]]:
    examples = []
    for name in sorted(tree):
        examples.append(tree[name][0])

    indicies: Dict[str, List[int]] = {
        'Washington': [],
        'WA Fish': [],
        'WA Inverts': [],
        'WA Algae': [],
    }

    for i, img in enumerate(examples):
        indicies['Washington'].append(i)
        indicies[f'WA {img.category}'].append(i)

    return indicies


def html_builder(css: str, game: str, data: str) -> str:
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
                <select id="game" onchange="choose_game(0);">
                    <option value="Washington">Washington</option>
                    <option value="WA Algae">WA Algae</option>
                    <option value="WA Fish">WA Fish</option>
                    <option value="WA Inverts">WA Inverts</option>
                </select>
                <div class="scoring">
                    <h3 id="score"></h3>
                    <h3 id="points"></h3>
                </div>
                <select id="difficulty" onchange="choose_game(0);">
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
            </div>
        </div>

        <footer>
            <p><a href="https://goto.anardil.net">goto.anardil.net</a></p>
            <p>austin@anardil.net 2024</p>
        </footer>

        <script>
            choose_game();
        </script>
    </body>
</html>
"""


def main() -> None:
    quality.record_all_dimensions(collection.load_images())

    limit = 20
    tree = species.build_image_tree()
    metrics.counter('images matched', sum(len(v) for v in tree.values()))

    tree = {k: tree[k][:limit] for k in list(tree)}
    metrics.counter('images used', sum(len(v) for v in tree.values()))
    metrics.counter('species short', sum(1 for v in tree.values() if len(v) < limit))
    metrics.counter('species represented', len(tree))

    writer(tree)

    images = [img for img_list in tree.values() for img in img_list]
    optimize.create_webp(images)
    metrics.summary()


if __name__ == '__main__':
    main()

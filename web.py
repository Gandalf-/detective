#!/usr/bin/python3

from typing import List, Tuple

from species import ImageTree, build_image_tree

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
        print('var names =', ns, file=fd)
        print('var thumbs =', ts, file=fd)
        print('var similarities =', ss, file=fd)
        print('var difficulties =', ds, file=fd)


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
        <link rel="stylesheet" href="/jquery.fancybox.min.css" />
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
                <a href="/timeline/">
                    <h1 class="top switch timeline">📅</h1>
                </a>
                <div class="top buffer"></div>
                <a href="/gallery/">
                    <h1 class="top switch gallery">📸</h1>
                </a>
                <div class="top buffer"></div>
                <a href="/detective/">
                    <h1 class="top switch detective">Detective</h1>
                </a>
                <div class="top buffer"></div>
                <a href="/sites/">
                    <h1 class="top switch sites">🌎</h1>
                </a>
                <div class="top buffer"></div>
                <a href="/taxonomy/">
                    <h1 class="top switch taxonomy">🔬</h1>
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

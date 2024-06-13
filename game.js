/* globals */
var g_correct = 0;
var g_incorrect = 0;
var g_points = 0;
var g_made_mistake = false;

var g_names = [];
var g_thumbs = [];
var g_similarities = [];

const g_lower_bound_table = [0, 15, 25, 40, 80];
const g_upper_bound_table = [10, 25, 35, 40, 100];
const g_count_table = [2, 2, 4, 6, 8];
const g_sample_table = [2, 2, 2, 1, 1];

/* game logic */

/*
 * the player is given a single image and must choose it's name from the
 * options below
 */
function name_game() {
    choose_dataset();

    const choices = get_choices();
    const correct = choose_correct(choices);

    const difficulty = get_difficulty();
    const lower_bound = g_lower_bound_table[difficulty];
    const upper_bound = g_upper_bound_table[difficulty];
    const count = g_count_table[difficulty];
    const options = find_similar(correct, lower_bound, upper_bound, count - 1);

    set_correct_name(correct, null, function() {
        reset_options();

        const actual = random(count);
        for (i = 0, w = 0; i < count; i++) {
            var child = document.createElement('div');
            child.setAttribute('id', 'option' + i);
            byId('options').appendChild(child);

            if (i == actual) {
                set_text('option' + i, correct, true);
            } else {
                set_text('option' + i, options[w], false);
                w++;
            }
        }

        add_zoom();
        add_skip();
        add_new_correct_thumbnail(correct);
    });
}

function blank_options() {
    for (i = 0; i < 8; i++) {
        var option = byId('option' + i);
        if (option == null) {
            continue;
        }
        if (option.hasAttribute('correct')) {
            option.style.border = "1px solid green";
        } else {
            option.innerHTML = '<h4>&nbsp;</h4>';
        }
    }
}

function choose_dataset() {
    g_names = data_names;
    g_thumbs = data_thumbs;
    g_similarities = data_similarities;
    g_people = data_people;
    g_credit = data_credit;
    g_categories = data_categories;
}

/* HTML modifying utilities */

g_delaying = false;

function choose_game(delay) {
    if (g_delaying) {
        return;
    }

    g_delaying = true;
    blank_options();
    console.log("waiting", delay, "ms");

    setTimeout(function() {
        g_made_mistake = false;
        update_score();
        name_game();
        g_delaying = false;
    }, delay);
}

function set_text(where, what, correct) {
    var option = byId(where);
    var name = g_names[what];

    if (correct) {
        option.setAttribute('correct', '');
    }

    option.setAttribute('onclick', 'selection(this)');
    option.setAttribute('class', 'top switch');

    var child = document.createElement('h4');
    child.innerHTML = name;

    option.innerHTML = '';
    option.appendChild(child);
}

function update_score() {
    var total = g_correct + g_incorrect;
    var score = 0;

    if (total != 0) {
        score = Math.floor(g_correct / total * 100);
    }

    byId('score').innerHTML = score + '% (' + g_correct + '/' + total + ')';
    byId('points').innerHTML = `Points: ${g_points.toLocaleString()}`;
}

function selection(where) {
    if (where.hasAttribute('correct')) {
        success(where);
    } else {
        failure(where);
    }
}

function success(where) {
    where.style.border = "1px solid green";
    g_correct++;

    if (!g_made_mistake) {
        const points = Math.pow(10, 1 + get_difficulty());
        console.log(`adding ${points} points for ${get_difficulty()}`)
        g_points += points;
    }

    choose_game(1000);
}

/**
 * Called when the player makes a mistake.
 * @param {HTMLElement} where - The element that was clicked.
 */
function failure(where) {
    where.style.border = "1px solid red";
    if (!g_made_mistake) {
        g_incorrect++;
        update_score();
    }
    g_made_mistake = true;
}

function reset_options() {
    byId('options').innerHTML = '';
}

/**
 * Hide the correct image but update the task for the player
 * @param {number} correct - The index of the correct creature.
 */
function set_thumbnail(where, what, thumb, person, callback) {
    var img = document.createElement('img');
    img.src = '/small/' + thumb + '.webp';

    var credit = document.createElement('p');
    credit.classList.add('credit');
    credit.innerHTML = `Photographer: ${person}`;

    img.onload = function() {
        const target = document.getElementById(where);
        target.innerHTML = '';
        target.appendChild(img);
        target.appendChild(credit);

        if (callback) {
            callback();
        }
    };
}

/**
 * Set the correct creature name and thumbnails on the game board.
 *
 * @param {number} correct - The index of the correct creature.
 * @param {string} previous - The last thumbnail hash, optional
 */
function set_correct_name(correct, previous, callback) {
    const images = shuffle([...g_thumbs[correct]]);

    var i = 0;
    while (i < images.length && images[i] === previous) {
        i++;
    }
    console.log('chose', images[i], 'as the correct image');

    const who = g_credit[correct][i];
    console.log('credit', g_people[who]);

    set_thumbnail(`correct`, correct, images[i], g_people[who], callback);
}

/*        _   _ _ _ _
 *  _   _| |_(_) (_) |_ _   _
 * | | | | __| | | | __| | | |
 * | |_| | |_| | | | |_| |_| |
 *  \__,_|\__|_|_|_|\__|\__, |
 *                      |___/
*/

/**
 * Add a "Skip" button to the options section.
 */
function add_skip() {
    const options = byId('options');

    const child = document.createElement('div');
    child.classList.add('top', 'switch', 'skip');
    child.addEventListener('click', function() {
        choose_game(1000);
    });
    child.innerHTML = '<h4 class="skip">Skip</h4>';

    options.appendChild(child);
}

/**
 * Add a "New Example" button to the options section. This is only for the name game.
 * @param {number} correct - The index of the correct creature.
 */
function add_new_correct_thumbnail(correct) {
    if (g_thumbs[correct].length < 2) {
        return;
    }

    const options = byId('options');

    function new_correct_thumbnail() {
        const current = byId('correct').firstChild.src.split('/').pop().split('.')[0];
        console.log('Setting a new correct thumbnail, previous was', current);
        set_correct_name(correct, current, null);
    }

    const child = document.createElement('div');
    child.classList.add('top', 'switch', 'skip');
    child.addEventListener('click', new_correct_thumbnail);
    child.innerHTML = '<h4 class="skip">New Example</h4>';

    options.appendChild(child);
}

/**
 * Add a "Zoom" button to the options section.
 * This replaces '/small/' with '/large/' in the image URL.
 */
function add_zoom() {
    const options = byId('options');

    function zoom() {
        const current = byId('correct').firstChild.src;
        var img = byId('correct').firstChild;

        img.src = current.replace('/small/', '/large/');
        img.style.maxWidth = '100%';
        img.style.height = 'auto';
    }

    const child = document.createElement('div');
    child.classList.add('top', 'switch', 'skip');
    child.addEventListener('click', zoom);
    child.innerHTML = '<h4 class="skip">Zoom</h4>';

    options.appendChild(child);
}

function get_choices() {
    const game = byId('game').value;
    return g_categories[game];
}

function get_difficulty() {
    return parseInt(byId('difficulty').value);
}

function set_difficulty(value) {
    byId('difficulty').value = value;
}

/**
 * Choose a creature index that matches the given difficulty level.
 *
 * @param {number} difficulty - The difficulty level to match.
 * @returns {number} The index of a creature that matches the difficulty level.
 */
function choose_correct(choices) {
    const choice = choices[random(choices.length)];
    console.log('choices', choices, choice, g_names[choice]);
    return choice;
}

/**
 * Find similar creatures as the provided target.
 *
 * The bounds restrict which creatures are valid candidates. A high minimum
 * similarity means only very similar creatures will be found. Likewise, a high
 * maximum similarity will make less similar creatures more likely.
 *
 * Both bounds will be relaxed if no candidates can be found until eventually
 * every creature will be considered.
 *
 * @param   {number} target - Index of the creature to find similar creatures for.
 * @param   {number} lowerBound - Minimum starting similarity.
 * @param   {number} upperBound - Maximum starting similarity.
 * @param   {number} required - How many creatures to find.
 * @returns {number[]} Array of creature indices.
 */
function find_similar(target, lowerBound, upperBound, required) {
    const found = [];
    var shuffledIndices = shuffle([...Array(g_names.length).keys()]);

    console.log("Search limits", lowerBound, upperBound, g_names[target]);

    while (found.length < required) {
        if (shuffledIndices.length === 0) {
            if (lowerBound <= 0 && upperBound >= 100) {
                console.error(
                    "Couldn't satisfy the requirement:", target, lowerBound, required);
                break;
            }

            // We've looped through, relax the constraints.
            lowerBound = Math.max(0, lowerBound - 5);
            upperBound = Math.min(100, upperBound + 5);
            console.log("New limits", lowerBound, upperBound);
            shuffledIndices = shuffle([...Array(g_names.length).keys()]);
        }

        const candidate = shuffledIndices.pop();
        if (candidate === target || found.includes(candidate)) {
            continue;
        }

        const i = Math.max(candidate, target);
        const j = Math.min(candidate, target);
        const score = g_similarities[i][j];

        if (score >= lowerBound && score <= upperBound) {
            found.push(candidate);
        }
    }

    found.forEach((creatureIndex, i) => {
        console.log(i, creatureIndex, g_names[creatureIndex]);
    });

    return found;
}


/* other utilities */

/**
 * Get a random integer between 0 and maximum.
 * @param {number} maximum - The maximum value possible.
 */
function random(maximum) {
    return Math.floor(Math.random() * 10 ** 5) % maximum
}

function byId(label) {
    return document.getElementById(label);
}

/**
 * Produce a shuffled version of the input array.
 * @param {any[]} array - The array to shuffle.
 */
function shuffle(array) {
    // https://stackoverflow.com/a/12646864

    const result = [...array];
    for (let i = result.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
}

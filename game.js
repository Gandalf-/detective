/* globals */
var g_correct = 0;
var g_incorrect = 0;
var g_points = 0;
var g_mistakes = 0;
var g_delaying = false;

/* constants */
const g_lower_bound_table = [0, 15, 25, 40, 80];
const g_upper_bound_table = [10, 25, 35, 40, 100];
const g_count_table = [2, 2, 4, 6, 8];
const g_sample_table = [2, 2, 2, 1, 1];

/**
 * Main entry point
 */
function choose_game(delay = 0) {
    if (g_delaying) {
        return;
    }
    g_delaying = true;

    blank_options();
    setTimeout(function() {
        g_mistakes = 0;
        update_score();
        name_game();
        g_delaying = false;
    }, delay);
}

/**
 * The player is given a single image and must choose it's name from the text options
 */
function name_game() {
    const correct = choose_correct(get_choices());

    const difficulty = get_difficulty();
    const lower_bound = g_lower_bound_table[difficulty];
    const upper_bound = g_upper_bound_table[difficulty];
    const count = g_count_table[difficulty];

    const incorrect = find_similar(correct, lower_bound, upper_bound, count - 1);

    set_correct_thumbnail(correct, null, function() {
        clear_options();

        const actual = random(count);
        for (i = 0, w = 0; i < count; i++) {
            var option = document.createElement('div');

            if (i == actual) {
                build_option(option, correct, true);
            } else {
                build_option(option, incorrect[w], false);
                w++;
            }

            byId('options').appendChild(option);
        }

        add_zoom();
        add_skip();
        add_new_correct_thumbnail(correct);
    });
}

/**
 * Build an option element for the name game.
 *
 * @param {HTMLElement} option - The element to build.
 * @param {number} name_index - The index of the creature's name.
 * @param {boolean} correct - Whether this is the correct option.
 */
function build_option(option, name_index, correct) {
    option.setAttribute('class', 'top switch');
    option.setAttribute('id', 'option' + i);

    if (correct) {
        option.setAttribute('correct', '');
        option.addEventListener('click', () => { success(option); });
    } else {
        option.addEventListener('click', () => { failure(option); });
    }

    var text = document.createElement('h4');
    text.innerHTML = g_names[name_index];

    option.innerHTML = '';
    option.appendChild(text);
}

function update_score() {
    var total = g_correct + g_incorrect;
    var score = 0;

    if (total != 0) {
        score = Math.floor(g_correct / total * 100);
    }

    byId('score').innerHTML = `${score}% (${g_correct}/${total})`;
    byId('points').innerHTML = `Points: ${g_points.toLocaleString()}`;
}

function success(where) {
    where.style.border = "1px solid green";

    if (g_mistakes == 0) {
        g_correct++;
    } else {
        g_incorrect++;
    }

    let points = Math.pow(10, 1 + get_difficulty());
    for (let i = 0; i < g_mistakes; i++) {
        points = Math.floor(points / 10);
    }
    console.log(`adding ${points} points for ${get_difficulty()}`)
    g_points += points;

    choose_game(1000);
}

function failure(where) {
    where.style.border = "1px solid red";
    g_mistakes++;
}

function clear_options() {
    byId('options').innerHTML = '';
}

/**
 * Blank out the options and highlight the correct one.
 */
function blank_options() {
    const options = document.getElementById('options').children;

    for (let option of options) {
        if (option.hasAttribute('correct')) {
            option.style.border = "1px solid green";
        } else {
            option.innerHTML = '<h4>&nbsp;</h4>';
        }
    }
}

/**
 * Set the thumbnail and credit for a target element.
 *
 * @param {HTMLElement} target - The element to set the thumbnail in.
 * @param {string} thumb - The thumbnail hash.
 * @param {string} person - The photographer's name.
 * @param {function} callback - Function to call after the thumbnail is loaded, optional.
 */
function set_thumbnail(target, thumb, person, callback) {
    var img = document.createElement('img');
    img.src = '/small/' + thumb + '.webp';

    var credit = document.createElement('p');
    credit.classList.add('credit');
    credit.innerHTML = `Photographer: ${person}`;

    img.onload = function() {
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
 * @param {string} previous - The last thumbnail hash, optional.
 * @param {function} callback - Function to call after the thumbnail is loaded, optional
 */
function set_correct_thumbnail(correct, previous, callback) {
    const images = shuffle([...g_thumbs[correct]]);
    var i = 0;
    while (i < images.length && images[i] === previous) {
        i++;
    }

    const image = images[i];
    const person_index = g_credit[correct][i];
    const credit = g_people[person_index];
    console.log('chose', image, credit, 'as the correct image');

    const target = document.getElementById('correct');
    set_thumbnail(target, image, credit, callback);
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
    const skip = document.createElement('div');
    skip.classList.add('top', 'switch', 'skip');
    skip.addEventListener('click', () => { choose_game(1000); });
    skip.innerHTML = '<h4 class="skip">Skip</h4>';

    byId('options').appendChild(skip);
}

/**
 * Add a "New Example" button to the options section. This is only for the name game.
 * @param {number} correct - The index of the correct creature.
 */
function add_new_correct_thumbnail(correct) {
    if (g_thumbs[correct].length < 2) {
        return;
    }

    function new_correct_thumbnail() {
        const current = byId('correct').firstChild.src.split('/').pop().split('.')[0];
        console.log('Setting a new correct thumbnail, previous was', current);
        set_correct_thumbnail(correct, current, null);
    }

    const child = document.createElement('div');
    child.classList.add('top', 'switch', 'skip');
    child.addEventListener('click', new_correct_thumbnail);
    child.innerHTML = '<h4 class="skip">New Example</h4>';

    byId('options').appendChild(child);
}

/**
 * Add a "Zoom" button to the options section.
 * This replaces '/small/' with '/large/' in the image URL.
 */
function add_zoom() {
    function enhance() {
        const current = byId('correct').firstChild.src;
        var img = byId('correct').firstChild;

        img.src = current.replace('/small/', '/large/');
        img.style.maxWidth = '100%';
        img.style.height = 'auto';
    }

    const zoom = document.createElement('div');
    zoom.classList.add('top', 'switch', 'skip');
    zoom.addEventListener('click', enhance);
    zoom.innerHTML = '<h4 class="skip">Zoom</h4>';

    byId('options').appendChild(zoom);
}

function get_choices() {
    const game = byId('game').value;
    return g_categories[game];
}

function get_difficulty() {
    return parseInt(byId('difficulty').value);
}

function choose_correct(choices) {
    return choices[random(choices.length)];
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
    console.log("search limits", lowerBound, upperBound, g_names[target]);

    while (found.length < required) {
        if (shuffledIndices.length === 0) {
            if (lowerBound <= 0 && upperBound >= 100) {
                console.error(
                    "couldn't satisfy the requirement:", target, lowerBound, required);
                break;
            }

            // We've looped through, relax the constraints.
            lowerBound = Math.max(0, lowerBound - 5);
            upperBound = Math.min(100, upperBound + 5);
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

/* globals */
var g_correct = 0;
var g_incorrect = 0;
var g_points = 0;
var g_mistakes = 0;
var g_delaying = false;

/* constants */
const g_lower_bound_table = [0, 15, 25, 50, 75];
const g_upper_bound_table = [10, 25, 50, 75, 100];
const g_count_table = [2, 2, 4, 6, 8];
const g_sample_table = [2, 2, 2, 1, 1];

/**
 * Main entry point — pick a new round, optionally after a delay.
 */
function choose_game(delay = 0) {
  if (g_delaying) return;
  g_delaying = true;

  blank_options();
  setTimeout(function () {
    g_mistakes = 0;
    update_score();
    name_game();
    g_delaying = false;
  }, delay);
}

/**
 * Build a round: pick a correct creature, find similar distractors,
 * load the photo, render the answer pills and action row.
 */
function name_game() {
  const correct = choose_correct(get_choices());

  const difficulty = get_difficulty();
  const lower_bound = g_lower_bound_table[difficulty];
  const upper_bound = g_upper_bound_table[difficulty];
  const count = g_count_table[difficulty];

  const incorrect = find_similar(correct, lower_bound, upper_bound, count - 1);

  set_correct_thumbnail(correct, null, function () {
    clear_options();
    clear_actions();

    const actual = random(count);
    for (let i = 0, w = 0; i < count; i++) {
      const option = document.createElement('div');
      if (i === actual) {
        build_option(option, correct, true, i);
      } else {
        build_option(option, incorrect[w], false, i);
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
 * Build an option pill.
 */
function build_option(option, name_index, correct, index) {
  option.className = 'pill';
  option.id = 'option' + index;

  if (correct) {
    option.setAttribute('correct', '');
    option.addEventListener('click', () => success(option));
  } else {
    option.addEventListener('click', () => failure(option));
  }

  const text = document.createElement('h4');
  text.textContent = g_names[name_index];
  option.appendChild(text);
}

function update_score() {
  const total = g_correct + g_incorrect;
  const score = total ? Math.floor((g_correct / total) * 100) : 0;
  byId('score').textContent = `${score}% (${g_correct}/${total})`;
  byId('points').textContent = `Points: ${g_points.toLocaleString()}`;
}

function success(where) {
  where.classList.remove('pill--wrong');
  where.classList.add('pill--correct');

  if (g_mistakes === 0) {
    g_correct++;
  } else {
    g_incorrect++;
  }

  let points = Math.pow(10, 1 + get_difficulty());
  for (let i = 0; i < g_mistakes; i++) {
    points = Math.floor(points / 10);
  }
  g_points += points;

  choose_game(1000);
}

function failure(where) {
  where.classList.add('pill--wrong');
  g_mistakes++;
}

function clear_options() {
  byId('options').innerHTML = '';
}

function clear_actions() {
  byId('actions').innerHTML = '';
}

/**
 * Blank the labels of all answer pills, mark the correct one.
 * Called between rounds while the new photo loads.
 */
function blank_options() {
  const options = byId('options').children;
  for (const option of options) {
    if (option.hasAttribute('correct')) {
      option.classList.add('pill--correct');
    } else {
      option.innerHTML = '<h4>&nbsp;</h4>';
    }
  }
}

/**
 * Insert a photo + photographer credit into the stage.
 */
function set_thumbnail(target, thumb, person, callback) {
  const src = '/small/' + thumb + '.webp';

  const img = document.createElement('img');
  img.alt = '';
  img.addEventListener('click', open_lightbox);

  const credit = document.createElement('p');
  credit.className = 'credit';
  credit.textContent = `Photographer: ${person}`;

  // Wire handlers BEFORE assigning src so a cached image still fires onload.
  img.onload = function () {
    target.innerHTML = '';
    target.style.setProperty('--photo-bg', `url('${src}')`);
    target.appendChild(img);
    target.appendChild(credit);
    if (callback) callback();
  };
  img.onerror = function () {
    console.error('failed to load', src);
    // Still advance — leaves the previous photo on stage but rebuilds options
    // so the user can interact (Skip will pick another image).
    if (callback) callback();
  };
  img.src = src;
}

/**
 * Pick a photo for the correct creature, avoiding the previous one if possible.
 */
function set_correct_thumbnail(correct, previous, callback) {
  const images = shuffle([...g_thumbs[correct]]);
  let i = 0;
  while (i < images.length && images[i] === previous) {
    i++;
  }

  const image = images[i];
  const person_index = g_credit[correct][i];
  const credit = g_people[person_index];

  set_thumbnail(byId('correct'), image, credit, callback);
}

/* ============================================================
   Action row buttons
   ============================================================ */

function add_skip() {
  const skip = document.createElement('button');
  skip.className = 'action';
  skip.type = 'button';
  skip.id = 'skip';
  skip.textContent = 'Skip';
  skip.addEventListener('click', () => choose_game(1000));
  byId('actions').appendChild(skip);
}

function add_new_correct_thumbnail(correct) {
  if (g_thumbs[correct].length < 2) return;

  const child = document.createElement('button');
  child.className = 'action';
  child.type = 'button';
  child.id = 'new_example';
  child.textContent = 'New Example';
  child.addEventListener('click', () => {
    const current = byId('correct').querySelector('img').src
      .split('/').pop().split('.')[0];
    set_correct_thumbnail(correct, current, null);
  });
  byId('actions').appendChild(child);
}

function add_zoom() {
  const zoom = document.createElement('button');
  zoom.className = 'action';
  zoom.type = 'button';
  zoom.id = 'zoom';
  zoom.textContent = 'Zoom';
  zoom.addEventListener('click', open_lightbox);
  byId('actions').appendChild(zoom);
}

/* ============================================================
   Lightbox
   ============================================================ */

function open_lightbox() {
  const img = byId('correct').querySelector('img');
  if (!img) return;
  byId('lightbox-img').src = img.src.replace('/small/', '/large/');
  byId('lightbox').hidden = false;
}

function close_lightbox() {
  byId('lightbox').hidden = true;
}

function toggle_lightbox() {
  if (byId('lightbox').hidden) {
    open_lightbox();
  } else {
    close_lightbox();
  }
}

/* ============================================================
   Keyboard
   ============================================================ */

function handle_key_down(event) {
  if (event.key === 'Escape') {
    if (!byId('lightbox').hidden) {
      close_lightbox();
      event.preventDefault();
    }
    return;
  }

  let option = null;
  switch (event.keyCode) {
    case 49: case 50: case 51: case 52: case 53:
    case 54: case 55: case 56: case 57: // 1-9
      if (!byId('lightbox').hidden) return;
      option = 'option' + (event.keyCode - 49);
      break;
    case 78: // n
      if (!byId('lightbox').hidden) return;
      option = 'new_example';
      break;
    case 83: // s
      if (!byId('lightbox').hidden) return;
      option = 'skip';
      break;
    case 90: // z
      toggle_lightbox();
      event.preventDefault();
      return;
  }

  if (option === null) return;
  const elem = byId(option);
  if (elem !== null) elem.click();
}

/* ============================================================
   Selection helpers
   ============================================================ */

function get_choices() {
  return g_categories[byId('game').value];
}

function get_difficulty() {
  return parseInt(byId('difficulty').value);
}

function choose_correct(choices) {
  return choices[random(choices.length)];
}

function incorrect_location(candidate) {
  if (!candidate.startsWith('Non-RC')) return false;

  const game = byId('game').value;
  const needed = game.substring(0, 2).toUpperCase();
  const actual = candidate.substring(6, 8);
  return actual !== needed;
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
 */
function find_similar(target, lowerBound, upperBound, required) {
  const found = [];
  let shuffledIndices = shuffle([...Array(g_names.length).keys()]);

  while (found.length < required) {
    if (shuffledIndices.length === 0) {
      if (lowerBound <= 0 && upperBound >= 100) {
        console.error("couldn't satisfy the requirement:", target, lowerBound, required);
        break;
      }
      lowerBound = Math.max(0, lowerBound - 5);
      upperBound = Math.min(100, upperBound + 5);
      shuffledIndices = shuffle([...Array(g_names.length).keys()]);
    }

    const candidate = shuffledIndices.pop();
    if (candidate === target || found.includes(candidate)) continue;
    if (incorrect_location(g_names[candidate])) continue;

    const i = Math.max(candidate, target);
    const j = Math.min(candidate, target);
    const score = g_similarities[i][j];

    if (score >= lowerBound && score <= upperBound) {
      found.push(candidate);
    }
  }

  return found;
}

/* ============================================================
   Misc
   ============================================================ */

function random(maximum) {
  return Math.floor(Math.random() * 10 ** 5) % maximum;
}

function byId(label) {
  return document.getElementById(label);
}

function shuffle(array) {
  // https://stackoverflow.com/a/12646864
  const result = [...array];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

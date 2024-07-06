# Merges hard-to-merge data using rapidfuzz, cython, pandas and numpy

### Tested against Windows 10 / Python 3.11 / Anaconda

### pip install rafuzzpandas

### Cython and a C compiler must be installed!


## Real world example - merging a list with common data (but not all data is in both lists)

```
# Input data:
# Rolling Stone Best Albums of All Time - 2021
first_list = r"""500 Kanye West, 'Stronger' 2007
499 The Supremes, 'Baby Love' 1964
498 Townes Van Zandt, 'Pancho and Lefty' 1972
497 Lizzo, 'Truth Hurts' 2017
496 Harry Nilsson, 'Without You' 1971
495 Carly Simon, 'You're So Vain' 1972
494 Cyndi Lauper, 'Time After Time' 1983
493 The Pixies, 'Where Is My Mind?' 1988
....
....
9 Fleetwood Mac, 'Dreams' 1977
8 Missy Elliott, 'Get Ur Freak On' 2001
7 The Beatles, 'Strawberry Fields Forever' 1967
6 Marvin Gaye, 'What’s Going On' 1971
5 Nirvana, 'Smells Like Teen Spirit' 1991
4 Bob Dylan, 'Like a Rolling Stone' 1965
3 Sam Cooke, 'A Change Is Gonna Come' 1964
2 Public Enemy, 'Fight the Power' 1989
1 Aretha Franklin, 'Respect' 1967"""



# Rolling Stone - best albums of all time - 2004 (different format, no quotes)
second_list = """1. Bob Dylan - Like a Rolling Stone
2. The Rolling Stones - Satisfaction
3. John Lennon - Imagine
4. Marvin Gaye - What’s Going On
5. Aretha Franklin - Respect
....
....
495. Smokey Robinson and the Miracles - Shop Around
496. The Rolling Stones - Miss You
497. Weezer - Buddy Holly
498. Brook Benton - Rainy Night in Georgia
499. Thin Lizzy - The Boys Are Back in Town
500. Boston - More Than a Feeling"""


# Merged Output
-----------------------------------------result1
MAPS ONE TO ONE - NO DUPLICATES

Smokey Robinson and the Miracles - The Tracks of My Tears-----Smokey Robinson and the Miracles, 'The Tracks of My Tears'
Grandmaster Flash and the Furious Five - The Message-----Grandmaster Flash and the Furious Five, 'The Message'
The Velvet Underground - I’m Waiting for the Man-----The Velvet Underground, 'I’m Waiting for the Man'
Martha and the Vandellas - Dancing in the Street-----Martha and the Vandellas, 'Dancing in the Street'
Simon and Garfunkel - Bridge Over Troubled Water-----Simon and Garfunkel, 'Bridge Over Troubled Water'
Sly and the Family Stone - Everyday People-----Sly and the Family Stone, 'Everyday People'
Screamin’ Jay Hawkins - I Put a Spell on You-----Screamin’ Jay Hawkins, 'I Put a Spell on You'
Marvin Gaye - I Heard It Through the Grapevine-----Marvin Gaye, 'I Heard It Through the Grapevine'
U2 - I Still Haven’t Found What I’m Looking For-----U2, 'I Still Haven’t Found What I’m Looking For'
Gladys Knight and the Pips - Midnight Train to Georgia-----Gladys Knight and the Pips, 'Midnight Train to Georgia'


-----------------------------------------result2
VALUES MIGHT BE DUPLICATES SOMEWHERE IN THE RESULTS

Smokey Robinson and the Miracles - The Tracks of My Tears-----Smokey Robinson and the Miracles, 'The Tracks of My Tears'
Grandmaster Flash and the Furious Five - The Message-----Grandmaster Flash and the Furious Five, 'The Message'
The Velvet Underground - I’m Waiting for the Man-----The Velvet Underground, 'I’m Waiting for the Man'
Martha and the Vandellas - Dancing in the Street-----Martha and the Vandellas, 'Dancing in the Street'
Simon and Garfunkel - Bridge Over Troubled Water-----Simon and Garfunkel, 'Bridge Over Troubled Water'
Sly and the Family Stone - Everyday People-----Sly and the Family Stone, 'Everyday People'
Screamin’ Jay Hawkins - I Put a Spell on You-----Screamin’ Jay Hawkins, 'I Put a Spell on You'
Marvin Gaye - I Heard It Through the Grapevine-----Marvin Gaye, 'I Heard It Through the Grapevine'
U2 - I Still Haven’t Found What I’m Looking For-----U2, 'I Still Haven’t Found What I’m Looking For'
Gladys Knight and the Pips - Midnight Train to Georgia-----Gladys Knight and the Pips, 'Midnight Train to Georgia'


-----------------------------------------result3
BEST RESULTS - MAPS ONE TO ONE - NO DUPLICATES

Smokey Robinson and the Miracles - The Tracks of My Tears-----Smokey Robinson and the Miracles, 'The Tracks of My Tears'
Grandmaster Flash and the Furious Five - The Message-----Grandmaster Flash and the Furious Five, 'The Message'
The Velvet Underground - I’m Waiting for the Man-----The Velvet Underground, 'I’m Waiting for the Man'
Martha and the Vandellas - Dancing in the Street-----Martha and the Vandellas, 'Dancing in the Street'
Simon and Garfunkel - Bridge Over Troubled Water-----Simon and Garfunkel, 'Bridge Over Troubled Water'

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

SECOND BEST RESULTS- MAPS ONE TO ONE - NO DUPLICATES

Bruce Springsteen - Thunder Road-----Bruce Springsteen, 'Jungleland'
David Bowie - Heroes-----David Bowie, 'Life on Mars?'
The Beatles - Let It Be-----The Strokes, 'Last Nite'
The Supremes - Baby Love-----The Supremes, 'Stop! In the Name of Love'
The Beatles - I Want to Hold Your Hand-----Tears for Fears, 'Everybody Wants to Rule the World'


-----------------------------------------result4
BEST RESULTS - VALUE MIGHT BE DUPLICATE

Smokey Robinson and the Miracles - The Tracks of My Tears-----Smokey Robinson and the Miracles, 'The Tracks of My Tears'
Grandmaster Flash and the Furious Five - The Message-----Grandmaster Flash and the Furious Five, 'The Message'
The Velvet Underground - I’m Waiting for the Man-----The Velvet Underground, 'I’m Waiting for the Man'
Martha and the Vandellas - Dancing in the Street-----Martha and the Vandellas, 'Dancing in the Street'
Simon and Garfunkel - Bridge Over Troubled Water-----Simon and Garfunkel, 'Bridge Over Troubled Water'

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

SECOND BEST RESULTS- VALUE MIGHT BE DUPLICATE - BUT NOT THE SAME KEY-VALUE COMBINATION LIKE THE FIRST

The Beatles - In My Life-----The Beatles, 'A Day in the Life'
The Beatles - A Day in the Life-----The Beatles, 'In My Life'
Bruce Springsteen - Thunder Road-----Bruce Springsteen, 'Jungleland'
Marvin Gaye - Let’s Get It On-----Marvin Gaye, 'What’s Going On'
David Bowie - Heroes-----David Bowie, 'Changes'
```

## How to use it

```PY

Finds the closest matches to the query strings from the choices using fuzzy string matching.

Parameters:
query_strings: The list (iterable) of query strings. DO NOT PUT EMPTY STRINGS IN THE LIST!
choices: The list (iterable) of choices to match against. DO NOT PUT EMPTY STRINGS IN THE LIST!
clear_cache (bool): Whether to clear the cache after processing.
max_results_each_query (int): The maximum number of results for each query.
allow_repeating_matches (bool): Whether to allow repeating matches.
first_limit (int): The initial score limit (presearch) for matches.
chunksize (int): The size of chunks to process.
cutoff (float): The score cutoff for matches.
processor (callable): The processor function to use.
score_cutoff (float): The score cutoff for matches.
score_hint (float): The score hint for matches.
score_multiplier (int): The score multiplier for matches.
workers (int): The number of workers to use.
scorer_kwargs (dict): Additional arguments for the scoring functions.
first_scorers (tuple): The tuple of scoring functions to use.

Returns:
dict: A dictionary containing the closest matches for each query.


from rafuzzpandas import get_closest_matches
import os

this_path = os.path.dirname(os.path.abspath(__file__))



rollingstone2021 = os.path.join(this_path, "rollingstone2021.txt")
rollingstone2004 = os.path.join(this_path, "rollingstone2004.txt")
with open(rollingstone2021, "r", encoding="utf-8") as f:
    first_list = f.read()
with open(rollingstone2004, "r", encoding="utf-8") as f:
    second_list = f.read()

# Little pre-processing to get rid of the numbers 
query_strings = [
    h
    for q in first_list.strip().splitlines()
    if (h := q.split(maxsplit=1)[-1].strip().rsplit(maxsplit=1)[0].strip())
]
choices = [
    h
    for q in second_list.strip().splitlines()
    if (h := q.split(maxsplit=1)[-1].strip())
]
for indi in range(10):
    print(f"{query_strings[indi]} ------ {choices[indi]}")

result1 = get_closest_matches(
    query_strings,
    choices,
    max_results_each_query=1,
    allow_repeating_matches=False,
    first_limit=70,
    chunksize=150,
    workers=1,
    scorer_kwargs=None,
    first_scorers=(
        "ratio",
        "partial_ratio",
        "token_sort_ratio",
        "token_set_ratio",
        "token_ratio",
        "partial_token_sort_ratio",
        "partial_token_set_ratio",
        "partial_token_ratio",
        "WRatio",
        "QRatio",
    ),
)
print("\n\n-----------------------------------------result1")
print("MAPS ONE TO ONE - NO DUPLICATES\n")
counter = 0
for k, v in result1[0].items():
    print(f"{k}-----{v}")
    counter += 1
    if counter == 10:
        break

result2 = get_closest_matches(
    query_strings,
    choices,
    max_results_each_query=1,
    allow_repeating_matches=True,
    first_limit=70,
    chunksize=150,
    workers=1,
    scorer_kwargs=None,
    first_scorers=(
        "ratio",
        "partial_ratio",
        "token_sort_ratio",
        "token_set_ratio",
        "token_ratio",
        "partial_token_sort_ratio",
        "partial_token_set_ratio",
        "partial_token_ratio",
        "WRatio",
        "QRatio",
    ),
)

print("\n\n-----------------------------------------result2")
print("VALUES MIGHT BE DUPLICATES SOMEWHERE IN THE RESULTS\n")
counter = 0
for k, v in result2[0].items():
    print(f"{k}-----{v}")
    counter += 1
    if counter == 10:
        break

result3 = get_closest_matches(
    query_strings,
    choices,
    max_results_each_query=3,
    allow_repeating_matches=False,
    first_limit=70,
    chunksize=150,
    workers=1,
    scorer_kwargs=None,
    first_scorers=(
        "ratio",
        "partial_ratio",
        "token_sort_ratio",
        "token_set_ratio",
        "token_ratio",
        "partial_token_sort_ratio",
        "partial_token_set_ratio",
        "partial_token_ratio",
        "WRatio",
        "QRatio",
    ),
)
print("\n\n-----------------------------------------result3")
print("BEST RESULTS - MAPS ONE TO ONE - NO DUPLICATES\n")
counter = 0
for k, v in result3[0].items():
    print(f"{k}-----{v}")
    counter += 1
    if counter == 5:
        break
print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")
print("SECOND BEST RESULTS- MAPS ONE TO ONE - NO DUPLICATES\n")
counter = 0
for k, v in result3[1].items():
    print(f"{k}-----{v}")
    counter += 1
    if counter == 5:
        break


result4 = get_closest_matches(
    query_strings,
    choices,
    max_results_each_query=3,
    allow_repeating_matches=True,
    first_limit=70,
    chunksize=150,
    workers=1,
    scorer_kwargs=None,
    first_scorers=(
        "ratio",
        "partial_ratio",
        "token_sort_ratio",
        "token_set_ratio",
        "token_ratio",
        "partial_token_sort_ratio",
        "partial_token_set_ratio",
        "partial_token_ratio",
        "WRatio",
        "QRatio",
    ),
)
print("\n\n-----------------------------------------result4")
print("BEST RESULTS - VALUE MIGHT BE DUPLICATE\n")
counter = 0
for k, v in result4[0].items():
    print(f"{k}-----{v}")
    counter += 1
    if counter == 5:
        break
print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n")

print(
    "SECOND BEST RESULTS- VALUE MIGHT BE DUPLICATE - BUT NOT THE SAME KEY-VALUE COMBINATION LIKE THE FIRST\n"
)
counter = 0
for k, v in result4[1].items():
    print(f"{k}-----{v}")
    counter += 1
    if counter == 5:
        break


```
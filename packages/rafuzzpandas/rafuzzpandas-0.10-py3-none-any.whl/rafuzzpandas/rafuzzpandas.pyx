import cython
cimport cython
import numpy as np
cimport numpy as np
np.import_array()
import rapidfuzz
import pandas as pd
from normaltext import lookup
import unicodedata
from math import ceil
from functools import cache
import re

cdef:
    dict fuzzlookupdict = {
        "ratio": rapidfuzz.fuzz.ratio,
        "partial_ratio": rapidfuzz.fuzz.partial_ratio,
        "token_sort_ratio": rapidfuzz.fuzz.token_sort_ratio,
        "token_set_ratio": rapidfuzz.fuzz.token_set_ratio,
        "token_ratio": rapidfuzz.fuzz.token_ratio,
        "partial_token_sort_ratio": rapidfuzz.fuzz.partial_token_sort_ratio,
        "partial_token_set_ratio": rapidfuzz.fuzz.partial_token_set_ratio,
        "partial_token_ratio": rapidfuzz.fuzz.partial_token_ratio,
        "WRatio": rapidfuzz.fuzz.WRatio,
        "QRatio": rapidfuzz.fuzz.QRatio,
    }

re_all_non_word_chars = re.compile(r'\W+', flags=re.I)
regexforspace = re.compile(r"\s+", flags=re.I)
regexfornonchars = re.compile(r"\W+", flags=re.I)
regex_no_repeating_letters = re.compile(
    r"(.)\1+", flags=re.I
)

def delete_fuzzystringmatching_cache():
    """
    Clears the cache for all cached fuzzy string matching functions.
    """
    unicode_normalize_nfd.cache_clear()
    unicode_normalize_nfc.cache_clear()
    unicode_normalize_nfkd.cache_clear()
    unicode_normalize_nfkc.cache_clear()
    preprocess_fuzz_and_no_accents.cache_clear()
    preprocess_no_accents.cache_clear()
    cached_compare.cache_clear()
    alllettersorted.cache_clear()
    rapidfuzz_utils_default_proces.cache_clear()
    remove_all_non_word_chars.cache_clear()
    get_no_spaces_string.cache_clear()
    unique_letters_sorted.cache_clear()
    strings_with_max_one_space.cache_clear()
    no_repeating_letters.cache_clear()
    threetimesregex.cache_clear()

@cache
def unicode_normalize_nfd(sen):
    """
    Normalizes a string using NFD (Normalization Form D).

    Parameters:
    sen (str): The string to normalize.

    Returns:
    str: The normalized string.
    """
    try:
        return unicodedata.normalize("NFD", sen)
    except Exception:
        return sen

@cache
def unicode_normalize_nfc(sen):
    """
    Normalizes a string using NFC (Normalization Form C).

    Parameters:
    sen (str): The string to normalize.

    Returns:
    str: The normalized string.
    """
    try:
        return unicodedata.normalize("NFC", sen)
    except Exception:
        return sen

@cache
def unicode_normalize_nfkd(sen):
    """
    Normalizes a string using NFKD (Normalization Form KD).

    Parameters:
    sen (str): The string to normalize.

    Returns:
    str: The normalized string.
    """
    try:
        return unicodedata.normalize("NFKD", sen)
    except Exception:
        return sen

@cache
def unicode_normalize_nfkc(sen):
    """
    Normalizes a string using NFKC (Normalization Form KC).

    Parameters:
    sen (str): The string to normalize.

    Returns:
    str: The normalized string.
    """
    try:
        return unicodedata.normalize("NFKC", sen)
    except Exception:
        return sen

@cache
def preprocess_fuzz_and_no_accents(sen, replace_char=""):
    """
    Preprocesses a string for fuzzy matching and removes accents.

    Parameters:
    sen (str): The string to preprocess.
    replace_char (str): The character to replace accents with.

    Returns:
    str: The preprocessed string.
    """
    return rapidfuzz.utils.default_process(
        "".join(
            [
                lookup(k, case_sens=True, replace=replace_char, add_to_printable="")[
                    "suggested"
                ]
                for k in sen
            ]
        )
    )

@cache
def preprocess_no_accents(sen, replace_char=""):
    """
    Preprocesses a string by removing accents.

    Parameters:
    sen (str): The string to preprocess.
    replace_char (str): The character to replace accents with.

    Returns:
    str: The preprocessed string.
    """
    try:
        return "".join(
            [
                lookup(k, case_sens=True, replace=replace_char, add_to_printable="")[
                    "suggested"
                ]
                for k in sen
            ]
        )
    except Exception:
        return sen

@cache
def cached_compare(s1, s2, processor):
    """
    Compares two strings using a specified fuzzy matching processor.

    Parameters:
    s1 (str): The first string.
    s2 (str): The second string.
    processor (str): The fuzzy matching processor to use.

    Returns:
    int: The similarity score.
    """
    return int(fuzzlookupdict[processor](s1, s2))

@cache
def alllettersorted(sen):
    """
    Sorts all characters in a string.

    Parameters:
    sen (str): The string to sort.

    Returns:
    str: The sorted string.
    """
    try:
        return ''.join(sorted((sen)))
    except Exception:
        return sen

def fuzzystringmatching(
    query_strings,
    choices_strings,
    tuple[str] scorers=(
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
    cython.uchar limit=90,
    Py_ssize_t chunksize=100,
    processor=None,
    score_cutoff=None,
    score_hint=None,
    Py_ssize_t score_multiplier=1,
    Py_ssize_t workers=1,
    scorer_kwargs=None,
):
    """
    Performs fuzzy string matching between query strings and choice strings.

    Parameters:
    query_strings (list): The list of query strings.
    choices_strings (list): The list of choice strings.
    scorers (tuple): The tuple of scoring functions to use.
    limit (cython.uchar): The score limit for matches.
    chunksize (Py_ssize_t): The size of chunks to process.
    processor (callable): The processor function to use.
    score_cutoff (float): The score cutoff for matches.
    score_hint (float): The score hint for matches.
    score_multiplier (Py_ssize_t): The score multiplier for matches.
    workers (Py_ssize_t): The number of workers to use.
    scorer_kwargs (dict): Additional arguments for the scoring functions.

    Returns:
    pd.DataFrame: The DataFrame containing the matching results.
    """
    cdef:
        np.ndarray choices, allqueries, choicesbytes, queriesbytes, ressfull
        cython.uchar[:, :]  ress
        Py_ssize_t choice_index, splitindexarray, query_index,  scorernameindex, scorerslen
        list[dict] resultdictlist
        float whole_len_all_queries
        Py_ssize_t nr_of_chunks, splitarrays_len, offset
        list[nd.ndarray] splitarrays
    scorerslen = len(scorers)
    choices = np.array(choices_strings)
    allqueries = np.array(query_strings)
    ressfull = np.array([], dtype=np.uint8)
    choicesbytes = np.fromiter(
        (
            b"".join(q)
            for q in choices.view("U1").reshape((choices.size, -1)).view("S4")
        ),
        dtype=f"S{choices.itemsize}",
    )
    resultdictlist = []
    whole_len_all_queries = len(allqueries)
    nr_of_chunks = ceil(whole_len_all_queries / chunksize)
    splitarrays = np.array_split(allqueries, nr_of_chunks)
    splitarrays_len = len(splitarrays)
    offset = 0
    for splitindexarray in range(splitarrays_len):
        queriesbytes = np.fromiter(
            (
                b"".join(q)
                for q in splitarrays[splitindexarray].view("U1").reshape((splitarrays[splitindexarray].size, -1)).view("S4")
            ),
            dtype=f"S{splitarrays[splitindexarray].itemsize}",
        )
        for scorernameindex in range(scorerslen):
            ressfull = rapidfuzz.process.cdist(
                queriesbytes,
                choicesbytes,
                scorer=fuzzlookupdict[scorers[scorernameindex]],
                processor=processor,
                score_cutoff=score_cutoff,
                score_hint=score_hint,
                score_multiplier=score_multiplier,
                dtype=np.uint8,
                workers=workers,
                scorer_kwargs=scorer_kwargs,
            )
            ress = ressfull
            for choice_index in range(ressfull.shape[1]):
                for query_index in range(ressfull.shape[0]):
                    if ress[query_index, choice_index] >= limit:
                        resultdictlist.append(
                            {
                                "score": ress[query_index, choice_index],
                                "scorer": scorers[scorernameindex],
                                "choice_string": choices[choice_index],
                                "query_string": splitarrays[splitindexarray][query_index],
                                "choice_index": choice_index,
                                "query_index": query_index + offset,
                                "LCSseq_similarity": rapidfuzz.distance.LCSseq.similarity(
                                    choicesbytes[choice_index],
                                    queriesbytes[query_index],
                                    score_cutoff=None,
                                ),
                                "LCSseq_distance_normalized_similarity": rapidfuzz.distance.LCSseq.normalized_similarity(
                                    choicesbytes[choice_index],
                                    queriesbytes[query_index],
                                    score_cutoff=None,
                                ),
                                "OSA_similarity": rapidfuzz.distance.OSA.similarity(
                                    choicesbytes[choice_index],
                                    queriesbytes[query_index],
                                    score_cutoff=None,
                                ),
                                "OSA_distance_normalized_similarity": rapidfuzz.distance.OSA.normalized_similarity(
                                    choicesbytes[choice_index],
                                    queriesbytes[query_index],
                                    score_cutoff=None,
                                ),
                                "Prefix_similarity": rapidfuzz.distance.Prefix.similarity(
                                    choicesbytes[choice_index],
                                    queriesbytes[query_index],
                                    score_cutoff=None,
                                ),
                                "Prefix_distance_normalized_similarity": rapidfuzz.distance.Prefix.normalized_similarity(
                                    choicesbytes[choice_index],
                                    queriesbytes[query_index],
                                    score_cutoff=None,
                                ),
                                "Postfix_similarity": rapidfuzz.distance.Postfix.similarity(
                                    choicesbytes[choice_index],
                                    queriesbytes[query_index],
                                    score_cutoff=None,
                                ),
                                "Postfix_distance_normalized_similarity": rapidfuzz.distance.Postfix.normalized_similarity(
                                    choicesbytes[choice_index],
                                    queriesbytes[query_index],
                                    score_cutoff=None,
                                ),
                            }
                        )

        offset += ressfull.shape[0]
    df = pd.DataFrame(resultdictlist)
    df.columns = [f"aa_{iq}" for iq in df.columns]
    df.loc[:, "aa_group_id"] = df.groupby(
        [
            "aa_choice_index",
            "aa_query_index",
        ]
    ).ngroup()
    return df

@cache
def rapidfuzz_utils_default_proces(sen):
    """
    Processes a string using rapidfuzz's default process.

    Parameters:
    sen (str): The string to process.

    Returns:
    str: The processed string.
    """
    try:
        return rapidfuzz.utils.default_process(sen)
    except Exception:
        return sen

@cache
def remove_all_non_word_chars(sen):
    """
    Removes all non-word characters from a string.

    Parameters:
    sen (str): The string to process.

    Returns:
    str: The processed string.
    """
    try:
        return regexfornonchars.sub("", sen)
    except Exception:
        return sen

@cache
def get_no_spaces_string(sen):
    """
    Removes all spaces from a string.

    Parameters:
    sen (str): The string to process.

    Returns:
    str: The processed string.
    """
    try:
        return regexforspace.sub("", sen)
    except Exception:
        return sen

@cache
def unique_letters_sorted(sen):
    """
    Sorts the unique characters in a string.

    Parameters:
    sen (str): The string to process.

    Returns:
    str: The processed string.
    """
    try:
        return "".join(sorted(set(sen)))
    except Exception:
        return sen

@cache
def strings_with_max_one_space(sen):
    """
    Reduces all spaces in a string to a single space.

    Parameters:
    sen (str): The string to process.

    Returns:
    str: The processed string.
    """
    try:
        return regexforspace.sub(" ", sen).strip()
    except Exception:
        return sen

@cache
def no_repeating_letters(sen):
    """
    Removes repeating characters from a string.

    Parameters:
    sen (str): The string to process.

    Returns:
    str: The processed string.
    """
    try:
        return regex_no_repeating_letters.sub(r"\1", sen)
    except Exception:
        return sen

@cache
def threetimesregex(sen):
    """
    Repeats each character in a string three times.

    Parameters:
    sen (str): The string to process.

    Returns:
    str: The processed string.
    """
    try:
        return "".join(x * 3 for x in sen)
    except Exception:
        return sen

def get_closest_matches(
    query_strings,
    choices,
    bint clear_cache=True,
    int max_results_each_query=5,
    bint allow_repeating_matches=False,
    int first_limit=50,
    int chunksize=100,
    cutoff=None,
    processor=None,
    score_cutoff=None,
    score_hint=None,
    int score_multiplier=1,
    int workers=4,
    scorer_kwargs=None,
    tuple[str] first_scorers=(
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
):
    """
    Finds the closest matches to the query strings from the choices using fuzzy string matching.

    Parameters:
    query_strings: The list of query strings.
    choices: The list of choices to match against.
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
    """
    cdef:
        np.ndarray arrayq, arrayc, all_new_columns_choices, all_new_columns_queries, column_queries_rev1, column_choices_rev1, item_aa_choice_string, item_aa_query_string
        Py_ssize_t colitemindex
        dict[Py_ssize_t, dict] dictresult_all
        bint allowed_more_than_one
        set[str] query_stringsx
        set[tuple[str]] query_stringsxtuple
        Py_ssize_t itemindex, kvx
        dict arraycachedict_queries, arraycachedict_choices
    arraycachedict_queries = {}
    arraycachedict_choices = {}
    dtype_rfuzz = np.float32
    arrayq = np.array(query_strings, dtype="U")
    arrayc = np.array(choices, dtype="U")
    df = fuzzystringmatching(
        arrayq,
        arrayc,
        scorers=(first_scorers),
        limit=first_limit,
        chunksize=chunksize,
        processor=processor,
        score_cutoff=cutoff,
        score_hint=score_hint,
        score_multiplier=score_multiplier,
        workers=workers,
        scorer_kwargs=scorer_kwargs,
    )

    df.loc[:, "cc_choices_unicode_normalized_nfc"] = df["aa_choice_string"].apply(
        unicode_normalize_nfc
    )
    df.loc[:, "cc_queries_unicode_normalized_nfc"] = df["aa_query_string"].apply(
        unicode_normalize_nfc
    )

    df.loc[:, "dd_choices_preprocess_rap"] = df["cc_choices_unicode_normalized_nfc"].apply(
        rapidfuzz_utils_default_proces
    )
    df.loc[:, "dd_queries_preprocess_rap"] = df["cc_queries_unicode_normalized_nfc"].apply(
        rapidfuzz_utils_default_proces
    )
    df.loc[:, "ee_choices_preprocess_no_accents"] = df["dd_choices_preprocess_rap"].apply(
        preprocess_no_accents
    )

    df.loc[:, "ee_queries_preprocess_no_accents"] = df["dd_queries_preprocess_rap"].apply(
        preprocess_no_accents
    )

    df.loc[:, "ff_choices_no_spaces"] = df["ee_choices_preprocess_no_accents"].apply(
        get_no_spaces_string
    )
    df.loc[:, "ff_queries_no_spaces"] = df["ee_queries_preprocess_no_accents"].apply(
        get_no_spaces_string
    )

    df.loc[:, "gg_choices_no_nonword_chars"] = df["ff_choices_no_spaces"].apply(
        remove_all_non_word_chars
    )

    df.loc[:, "gg_queries_no_nonword_chars"] = df["ff_queries_no_spaces"].apply(
        remove_all_non_word_chars
    )

    df.loc[:, "hh_choices_no_unique_chars"] = df["gg_choices_no_nonword_chars"].apply(
        unique_letters_sorted
    )

    df.loc[:, "hh_queries_no_unique_chars"] = df["gg_queries_no_nonword_chars"].apply(
        unique_letters_sorted
    )

    df.loc[:, "ii_choices_once_space"] = df["ee_choices_preprocess_no_accents"].apply(
        strings_with_max_one_space
    )

    df.loc[:, "ii_queries_once_space"] = df["ee_queries_preprocess_no_accents"].apply(
        strings_with_max_one_space
    )

    df.loc[:, "jj_choices_no_repeat"] = df["ii_choices_once_space"].apply(no_repeating_letters)

    df.loc[:, "jj_queries_no_repeat"] = df["ii_queries_once_space"].apply(no_repeating_letters)
    df.loc[:, "kk_choices_3_repeat"] = df["ii_choices_once_space"].apply(threetimesregex)

    df.loc[:, "kk_queries_3_repeat"] = df["ii_queries_once_space"].apply(threetimesregex)
    df.loc[:, "ll_choices_all_sorted_chars"] = df["gg_choices_no_nonword_chars"].apply(
        alllettersorted
    )

    df.loc[:, "ll_queries_all_sorted_chars"] = df["gg_queries_no_nonword_chars"].apply(
        alllettersorted
    )
    all_new_columns_choices = np.array(
        [
            "cc_choices_unicode_normalized_nfc",
            "dd_choices_preprocess_rap",
            "ee_choices_preprocess_no_accents",
            "ff_choices_no_spaces",
            "gg_choices_no_nonword_chars",
            "hh_choices_no_unique_chars",
            "ii_choices_once_space",
            "jj_choices_no_repeat",
            "kk_choices_3_repeat",
            'll_choices_all_sorted_chars'
        ]
    )
    all_new_columns_queries = np.array(
        [
            "cc_queries_unicode_normalized_nfc",
            "dd_queries_preprocess_rap",
            "ee_queries_preprocess_no_accents",
            "ff_queries_no_spaces",
            "gg_queries_no_nonword_chars",
            "hh_queries_no_unique_chars",
            "ii_queries_once_space",
            "jj_queries_no_repeat",
            "kk_queries_3_repeat",
            "ll_queries_all_sorted_chars"
        ]
    )

    df.insert(
        0,
        "aa_sum",
        np.zeros(len(df), dtype=dtype_rfuzz),
    )
    for scorer in fuzzlookupdict.values():
        for colitemindex in range(len(all_new_columns_queries)):
            df["aa_sum"] += rapidfuzz.process.cpdist(
                df[all_new_columns_choices[colitemindex]].__array__(),
                df[all_new_columns_queries[colitemindex]].__array__(),
                scorer=scorer,
                processor=processor,
                score_cutoff=score_cutoff,
                score_hint=score_hint,
                score_multiplier=score_multiplier,
                dtype=dtype_rfuzz,
                workers=workers,
                scorer_kwargs=scorer_kwargs,
            )

            if colitemindex not in arraycachedict_queries:
                column_queries_rev1 = np.array(df[all_new_columns_choices[colitemindex]].__array__().tolist(), dtype="U")
                arraycachedict_queries[colitemindex] = np.fromiter(
                    (q[:: len(q) - 1] for q in column_queries_rev1),
                    dtype=f"U{column_queries_rev1.itemsize //4}",
                )
            if colitemindex not in arraycachedict_choices:
                column_choices_rev1 = np.array(df[all_new_columns_queries[colitemindex]].__array__().tolist(), dtype="U")
                arraycachedict_choices[colitemindex] = np.fromiter(
                (q[:: len(q) - 1] for q in column_choices_rev1),
                dtype=f"U{column_choices_rev1.itemsize //4}",
            )
            df["aa_sum"] += rapidfuzz.process.cpdist(
                arraycachedict_queries[colitemindex],
                arraycachedict_choices[colitemindex],
                scorer=scorer,
                processor=processor,
                score_cutoff=score_cutoff,
                score_hint=score_hint,
                score_multiplier=score_multiplier,
                dtype=dtype_rfuzz,
                workers=workers,
                scorer_kwargs=scorer_kwargs,
            )

    df["aa_sum"] += (
        (df["aa_LCSseq_distance_normalized_similarity"] * 100)
        + df["aa_LCSseq_similarity"]
        + df["aa_OSA_similarity"]
        + df["aa_Prefix_similarity"]
        + df["aa_Postfix_similarity"]
    )
    df.sort_values(by="aa_sum", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)

    dictresult_all = {kv: {} for kv in range(max_results_each_query)}
    allowed_more_than_one = allow_repeating_matches
    query_stringsx = set()
    query_stringsxtuple = set()
    item_aa_choice_string = df.aa_choice_string.__array__()
    item_aa_query_string = df.aa_query_string.__array__()
    for itemindex in range(len(item_aa_choice_string)):
        for kvx in range(max_results_each_query):
            if item_aa_choice_string[itemindex] not in dictresult_all[kvx]:
                if not allowed_more_than_one:
                    if item_aa_query_string[itemindex] in query_stringsx:
                        continue
                if (
                    item_aa_choice_string[itemindex],
                    item_aa_query_string[itemindex],
                ) in query_stringsxtuple:
                    continue
                dictresult_all[kvx][item_aa_choice_string[itemindex]] = item_aa_query_string[
                    itemindex
                ]
                if not allowed_more_than_one:
                    query_stringsx.add(item_aa_query_string[itemindex])
                query_stringsxtuple.add(
                    (
                        item_aa_choice_string[itemindex],
                        item_aa_query_string[itemindex],
                    )
                )
                break
    if clear_cache:
        delete_fuzzystringmatching_cache()

    return dictresult_all

from .Trie import Trie
import re


# Trie regexp for efficient unioning
# argument is any python iteratable
def construct_trie(keywords):
    trie = Trie()
    for keyword in keywords:
        if type(keyword) != str:
            print("Err, non-string entry: ", keyword)
        else:
            trie.add(keyword)

    return trie


def construct_re(trie, include_space=False):
    keywords_re = r"(\b" + trie.pattern() + r"\b)"

    if include_space:
        keywords_re += r"|\s+"

    return re.compile(keywords_re, re.IGNORECASE)



def get_matches(inp_text, keywords_re, include_counts=False):
    keyword_matches = re.finditer(keywords_re, inp_text)
    keyword_matches = map(lambda s : s.group().lower(), keyword_matches)

    if include_counts:
        keyword_freqs = {}
        for keyword in keyword_matches:
            if keyword not in keyword_freqs:
                keyword_freqs[keyword] = 1
            else:
                keyword_freqs[keyword] += 1

        keyword_matches = sorted(keyword_freqs.items(), key=lambda t: t[1], reverse=True)
    else:
        keyword_matches = set(keyword_matches)

    return list(keyword_matches)


def get_matches_overlap(inp_text, trie, include_counts=False):
    word_start_re = re.compile(r"\b(\w)")

    word_boundries = word_start_re.finditer(inp_text)
    matches = set()

    keyword_freqs = {}
    for word_match in word_boundries:
        word_start_idx = word_match.start(1)

        curr_matches = trie.get_matches(inp_text, word_start_idx)
        matches = matches.union(curr_matches)

        for keyword in curr_matches:
            if keyword not in keyword_freqs:
                keyword_freqs[keyword] = 1
            else:
                keyword_freqs[keyword] += 1
    
    if include_counts:
        keyword_freq_ts = sorted(keyword_freqs.items(), key=lambda t: t[1], reverse=True)
        return keyword_freq_ts
    else:
        return list(matches)


if __name__ == "__main__":

    # Below variables should be defined and constructed only once
    keywords = ["machine", "machine learning", "machine learning algorithm", "learning", "learning algorithm", "algorithms", "algooooo"]
    kw_trie = construct_trie(keywords)


    # Sample use case @Jiaying
    # Get all overlapping keyword matches from an inp_text
    # (given a set of keywords)
    # returns a list of strs in matches variable
    inp_text = "This abstract is about machine learning algorithms."
    matches = get_matches_overlap(inp_text, kw_trie)
    print(matches)

# https://stackoverflow.com/questions/42742810/speed-up-millions-of-regex-replacements-in-python-3/42789508#42789508

import re


class Trie():
    """Regex::Trie in Python. Creates a Trie out of a list of words. The trie can be exported to a Regex pattern.
    The corresponding Regex should match much faster than a simple Regex union."""

    def __init__(self):
        self.data = {}

    def add(self, word):
        ref = self.data
        for char in word:
            ref[char] = char in ref and ref[char] or {}
            ref = ref[char]
        ref[''] = 1

    def dump(self):
        return self.data

    @staticmethod
    def quote(char):
        return re.escape(char)

    @staticmethod
    def _pattern(pData):
        data = pData
        if "" in data and len(data.keys()) == 1:
            return None

        alt = []
        cc = []
        q = 0
        for char in sorted(data.keys()):
            if isinstance(data[char], dict):
                try:
                    recurse = Trie._pattern(data[char])
                    alt.append(Trie.quote(char) + recurse)
                except:
                    cc.append(Trie.quote(char))
            else:
                q = 1
        cconly = not len(alt) > 0

        if len(cc) > 0:
            if len(cc) == 1:
                alt.append(cc[0])
            else:
                alt.append('[' + ''.join(cc) + ']')

        if len(alt) == 1:
            result = alt[0]
        else:
            result = "(?:" + "|".join(alt) + ")"

        if q:
            if cconly:
                result += "?"
            else:
                result = "(?:%s)?" % result
        return result


    def get_matches(self, inp_text, start_idx=0):

        matches = []
        curr_dict = self.data
        curr_idx = start_idx
        cuml_word = ""

        while curr_idx < len(inp_text) and curr_dict is not None:
            curr_char = inp_text[curr_idx]
            cuml_word += curr_char

            if curr_char in curr_dict:
                curr_dict = curr_dict[curr_char]

                if '' in curr_dict:
                    matches.append(cuml_word)
            else:
                curr_dict = None

            curr_idx += 1

        return matches


    @staticmethod
    def _keywords(kw_trie, prefix=''):
        if type(kw_trie) is not dict:
            return [prefix]

        elif len(kw_trie) == 1:
            next_key = list(kw_trie.keys())
            next_key = next_key[0]

            return Trie._keywords(kw_trie[next_key], prefix + next_key)

        else:
            res = []
            for k in kw_trie.keys():
                curr_res = Trie._keywords(kw_trie[k], prefix + k)
                res += curr_res

            return res


    @staticmethod
    def get_groups(kwd_trie, require_root=True):
        kw_groups = []

        def get_groups_helper(kwd_trie_loc, global_groups, prefix=''):
            if type(kwd_trie_loc) is not dict:
                global_groups.append([prefix])
                return

            grouped_root = False
            break_cond = ' ' in kwd_trie_loc
            if require_root:
                break_cond = break_cond and '' in kwd_trie_loc

            if break_cond:
                break_group = Trie._keywords(kwd_trie_loc[' '], prefix + ' ')
                break_group.append(prefix)
                global_groups.append(break_group)

                grouped_root = True

            for k in kwd_trie_loc:
                if not grouped_root or (k != ' ' and k != ''):
                    get_groups_helper(kwd_trie_loc[k], global_groups, prefix + k)

        get_groups_helper(kwd_trie, kw_groups)
        return kw_groups


    def pattern(self):
        return Trie._pattern(self.dump())

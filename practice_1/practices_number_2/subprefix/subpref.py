from typing import List


def brutforce(words: List[str]):
    max_length = 0
    answer = []
    for word1 in words:
        for word2 in words:
            if word1 == word2:
                continue
            min_len = max_length
            max_len = min(len(word2), len(word2))
            for pref in range(max_len, min_len, -1):
                if word2.endswith(word1[:pref]):
                    max_length = pref
                    answer = [word1, word2]
                    break
    return max_length, answer


def fast(words: List[str]):
    answer_length = 0
    answer = []
    prefixes = {}
    for word in words:
        for i in range(1, len(word) + 1):
            pref = word[:i]
            if pref not in prefixes:
                prefixes[pref] = set()
            prefixes[pref].add(word)

    for word2 in words:
        substr_found = False
        min_len = answer_length
        max_len = len(word2)
        for i in range(max_len, min_len, -1):
            substr = word2[-i:]
            if substr in prefixes:
                for word1 in prefixes[substr]:
                    if word1 == word2:
                        continue
                    answer_length = i
                    answer = [word1, word2]
                    break
            if substr_found:
                break

    return answer_length, answer

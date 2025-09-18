#!/usr/bin/env python3

import argparse
import random


def get_args():
    parser = argparse.ArgumentParser(
        usage='%(prog)s -l LEN -n N [OPTIONS]',
        description='Suffix-prefix input data generator',
        prefix_chars='-/')
    parser.add_argument(
        '-w', '--word',
        default='12345',
        metavar='WORD', type=str,
        help='answer (default: "12345")')
    parser.add_argument(
        '-l', '--length',
        metavar='LEN', type=int, required=True,
        help='maximum length')
    parser.add_argument(
        '-e', '--equal',
        action='store_true',
        help='length of all words will be equal')
    parser.add_argument(
        '-n', '--total',
        metavar='N', type=int, required=True,
        help='total words count')
    return (parser, parser.parse_args())


def check(word, length, all_suf, all_pref):
    for l in range(length, len(word)):
        if word[:l] in all_pref:
            return False
        if word[-l:] in all_suf:
            return False
    return True


def add_word(word, length, all_suf, all_pref):
    for l in range(length, len(word)):
        all_pref.add(word[:l])
        all_suf.add(word[-l:])


def generate(answer, length, total, equals):
    min_length = length if equals else len(answer) + 1
    max_length = length
    abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'

    pre_idx = random.randint(1, total)
    suf_idx = random.randint(1, total)
    if pre_idx == suf_idx:
        pre_idx = 1 + (pre_idx + 1) % total

    all_suffixes = set()
    all_prefixes = set()

    i = 1
    words = []
    while i <= total:
        word_len = random.randint(min_length, max_length)
        if i in [pre_idx, suf_idx]:
            word_len -= len(answer)

        word = ''.join(random.choice(abc) for _ in range(word_len))
        if i == pre_idx:
            word = answer + word
        if i == suf_idx:
            word = word + answer

        if check(word, len(answer), all_suffixes, all_prefixes):
            add_word(word, len(answer), all_suffixes, all_prefixes)
            words.append(word)
            i += 1
    return words


def main():
    parser, args = get_args()
    if args.length < len(args.word):
        parser.exit(1, 'invalid length')
    if args.total < 2:
        parser.exit(1, 'words count must be greater 2')
    if not args.word.isalnum():
        parser.exit(1, 'invalid word, must be alphanumeric')

    for word in generate(args.word, args.length, args.total, args.equal):
        print(word)


if __name__ == '__main__':
    main()
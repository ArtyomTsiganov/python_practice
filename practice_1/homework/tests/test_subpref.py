from typing import List

import pytest

from practice_1.homework.subprefix import subpref  # Я не понимаю почему оно не может нормально импортироваться
from practice_1.homework.generate_words import gen_words  # мне моя функция больше нравиться


def is_answer_correct(answer) -> bool:
    ln = answer[0]
    pref = answer[1][0]
    suff = answer[1][1]
    if pref[:ln] == suff[-ln:]:
        if ln == len(pref) or ln == len(suff):
            return True
        if pref[:ln + 1] != suff[-ln - 1:]:
            return True
    return False


def is_eq_answers(answer1, answer2):
    if is_answer_correct(answer1) and is_answer_correct(answer2):
        return answer1[0] == answer2[0]
    return False



@pytest.fixture()
def set_up_data() -> List[str]:
    with open("practice_1/homework/tests/assets/words_1k.txt", encoding="utf-8") as f:
        return f.read().split()


@pytest.mark.parametrize("words_count, expected_len", [
    (10, 2),
    (50, 2),
    (100, 2),
    (500, 4),
    (1000, 4),
])
def test_bruteforce(words_count: int, expected_len: int, set_up_data):
    data = set_up_data[:words_count]
    answer = subpref.brutforce(data)
    assert is_answer_correct(answer)
    assert answer[0] == expected_len


@pytest.mark.parametrize("words_count, expected_len", [
    (10, 2),
    (50, 2),
    (100, 2),
    (500, 4),
    (1000, 4),
])
def test_fast(words_count: int, expected_len: int, set_up_data):
    data = set_up_data[:words_count]
    answer = subpref.fast(data)
    assert is_answer_correct(answer)
    assert answer[0] == expected_len


def test_bruteforce_eq_fast_on_set_up(set_up_data):
    answer1 = subpref.brutforce(set_up_data)
    answer2 = subpref.fast(set_up_data)
    assert is_eq_answers(answer1, answer2)


@pytest.mark.repeat(100)
def test_bruteforce_eq_fast_20_words():
    data = gen_words(20)
    answer1 = subpref.brutforce(data)
    answer2 = subpref.fast(data)
    assert is_eq_answers(answer1, answer2)


@pytest.mark.repeat(25)
def test_bruteforce_eq_fast_200_words():
    data = gen_words(200)
    answer1 = subpref.brutforce(data)
    answer2 = subpref.fast(data)
    assert is_eq_answers(answer1, answer2)


@pytest.mark.repeat(10)
def test_bruteforce_eq_fast_4000_words():
    data = gen_words(2000)
    answer1 = subpref.brutforce(data)
    answer2 = subpref.fast(data)
    assert is_eq_answers(answer1, answer2)




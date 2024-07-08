from memotica.sm2 import sm2


def test_sm2_first_correct_recall():
    assert sm2(0, 2.5, 0, 4) == (1, 2.5, 1)


def test_sm2_second_correct_recall():
    assert sm2(1, 2.5, 1, 4) == (2, 2.5, 6)


def test_sm2_third_correct_recall():
    assert sm2(2, 2.5, 6, 4) == (3, 2.5, 15)


def test_sm2_incorrect_recall():
    assert sm2(2, 2.5, 6, 2) == (0, 2.34, 1)

import random
from tabulate import tabulate


class GameResult:
    def __init__(self, is_perfect: bool, num_prizes: int):
        self.is_perfect = is_perfect
        self.num_prizes = num_prizes


class TestResult:
    def __init__(self, name, perfect_percent, num_for_perfect, avg_num_prizes):
        self.name = name
        self.perfect_percent = perfect_percent
        self.num_for_perfect = num_for_perfect
        self.avg_num_prizes = avg_num_prizes


def play_with_no_bonuses():
    # last 4 must be mimics
    mimic_positions = sorted(random.sample(range(30), 4))
    is_perfect = mimic_positions[0] == 26
    num_prizes = mimic_positions[0]
    return GameResult(is_perfect, num_prizes)


def play_with_1x_shield():
    # last 4 must be mimics or 1st and last 3
    mimic_positions = sorted(random.sample(range(30), 4))
    is_perfect = mimic_positions[0] == 26 or (mimic_positions[0] == 0 and mimic_positions[1] == 27)
    num_prizes = None
    if mimic_positions[0] == 0:
        num_prizes = mimic_positions[1] - 1
    else:
        num_prizes = mimic_positions[0]
    return GameResult(is_perfect, num_prizes)


def play_with_1x_shield_and_saver():
    item_positions = sorted(random.sample(range(30), 5))
    # 0: Saver
    # 1-4: Mimics
    is_perfect = None
    num_prizes = None
    if item_positions[1] == 0:  # mimic caught by shield
        if item_positions[0] < item_positions[2]:  # saver before 2nd mimic
            is_perfect = item_positions[3] == 28  # last 2 are mimics
            num_prizes = item_positions[3] - 3  # minus 1 saver and 2 mimics
        else:
            is_perfect = False
            num_prizes = item_positions[2] - 1  # minus 1 mimic
    else:
        if item_positions[0] < item_positions[1]:  # saver before 1st mimic
            is_perfect = item_positions[2] == 27  # last 3 are mimics
            num_prizes = item_positions[2] - 2  # minus 1 saver and 1 mimic
        else:
            is_perfect = False
            num_prizes = item_positions[1]

    return GameResult(is_perfect, num_prizes)


def play_with_2x_shield_and_saver():
    item_positions = sorted(random.sample(range(30), 5))
    # 0: Saver
    # 1-4: Mimics
    is_perfect = None
    num_prizes = None
    num_mimics_caught_by_shields = 0
    if 0 in item_positions[1:]:
        num_mimics_caught_by_shields += 1
    if 1 in item_positions[1:]:
        num_mimics_caught_by_shields += 1

    if num_mimics_caught_by_shields == 0:  # mimic caught by shield
        if item_positions[0] < item_positions[1]:  # saver before 1st mimic
            is_perfect = item_positions[3] == 28  # last 2 are mimics
            num_prizes = item_positions[3] - 3  # minus 1 saver and 2 mimics
        else:
            is_perfect = False
            num_prizes = item_positions[2] - 1  # minus 1 mimic
    elif num_mimics_caught_by_shields == 1:
        if item_positions[0] < item_positions[1]:  # saver before 1st mimic
            is_perfect = item_positions[2] == 27  # last 3 are mimics
            num_prizes = item_positions[2] - 2  # minus 1 saver and 1 mimic
        else:
            is_perfect = False
            num_prizes = item_positions[1]
    else:  # num_mimics_caught_by_shields == 2
        if item_positions[0] < item_positions[2]:  # saver before 2nd mimic
            is_perfect = item_positions[3] == 28  # last 2 are mimics
            num_prizes = item_positions[3] - 3  # minus 1 saver and 2 mimics
        else:
            is_perfect = False
            num_prizes = item_positions[2] - 1  # minus 1 mimic

    return GameResult(is_perfect, num_prizes)


def run_test(name, play_method, num_trials):
    num_perfect = 0
    sum_prizes_opened = 0
    for i in range(num_trials):
        result = play_method()
        if result.is_perfect:
            num_perfect += 1
        sum_prizes_opened += result.num_prizes

    odds = num_perfect / num_trials
    avg_prizes = sum_prizes_opened / num_trials

    return TestResult(name, odds, round(1.0 // odds * 100), round(avg_prizes, 2))


def run_test_suite(num_trials=1_000_000):
    tests = {
        "No Bonuses": play_with_no_bonuses,
        "1x Shield": play_with_1x_shield,
        "1x Shield + Saver": play_with_1x_shield_and_saver,
        "2x Shield + Saver": play_with_2x_shield_and_saver
    }
    results = []
    for name, test_func in tests.items():
        result = run_test(name, test_func, num_trials)
        results.append(result)

    table_data = []
    for result in results:
        table_data.append([result.name, result.perfect_percent, result.num_for_perfect, result.avg_num_prizes])

    print(tabulate(table_data, headers=["NAME", "PERFECT %", "HUNTS/PERFECT", "AVG PRIZES"]))


run_test_suite()

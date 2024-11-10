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


# strategy: 1, 2 random, 3 saver
def play(num_shields: int = 0, include_saver: bool = False, include_x2: bool = False, kill_chance: float = 0, wait_strategy: bool = False, wait_num: int = 0):
    num_unknown_chests = 29 if include_saver else 30
    item_positions = random.sample(range(num_unknown_chests), 6)
    mimic_positions = item_positions[:4]
    x2_position = None if not include_saver else item_positions[4]
    is_perfect = True
    num_prizes = 0
    mimics_left = 4
    savers_left = 0
    saver_location_known = include_saver
    double_next = False
    for i in range(num_unknown_chests):
        if i < 2 and double_next and saver_location_known:
            # select the saver
            saver_location_known = False
            savers_left += 2
            num_shields -= 1  # because choosing the saver would use one of the shielded picks
            double_next = False
        if wait_strategy:
            if double_next and saver_location_known:
                saver_location_known = False
                savers_left += 2
                double_next = False
            elif wait_num > 0 and i == 2 + wait_num and saver_location_known:
                # select the saver
                saver_location_known = False
                savers_left += 1
        elif i == 2 and saver_location_known:
            # select the saver
            saver_location_known = False
            savers_left += 1

        if i in mimic_positions:
            if i <= num_shields - 1:  # blocked by shield
                mimics_left -= 1
            elif savers_left > 0:
                mimics_left -= 1
                if random.random() >= kill_chance:  # saver isn't used up if killed
                    savers_left -= 1
            else:
                if kill_chance > 0 and random.random() < kill_chance:
                    mimics_left -= 1
                else:
                    is_perfect = False
                    break
        elif include_x2 and i == x2_position:
            double_next = True
        else:
            num_prizes += 2 if double_next else 1
        if num_unknown_chests - i - 1 == mimics_left:
            break  # only mimics left, you win

    if is_perfect:
        num_prizes *= 3  # average reward from perfect chests

    return GameResult(is_perfect, num_prizes)


def play_with_no_bonuses():
    return play(0, False, False, 0)


def play_with_1x_shield():
    return play(1, False, False, 0)


def play_with_1x_shield_and_saver():
    return play(1, True, False, 0)


def play_with_2x_shield_and_saver():
    return play(2, True, False, 0)


def play_with_2x_shield_saver_and_x2():
    return play(2, True, True, 0)


def play_wait_strategy_with_2x_shield_saver_x2_and_1_kill_chance():
    return play(2, True, True, .01, True)


def play_wait_strategy_with_2x_shield_saver_x2_and_1_kill_chance_wait_1():
    return play(2, True, True, .01, True, wait_num=1)


def play_wait_strategy_with_2x_shield_saver_x2_and_1_kill_chance_wait_2():
    return play(2, True, True, .01, True, wait_num=2)


def play_wait_strategy_with_2x_shield_saver_x2_and_1_kill_chance_wait_3():
    return play(2, True, True, .01, True, wait_num=3)


def play_with_2x_shield_saver_and_1_kill_chance():
    return play(2, True, True, .01)


def play_with_2x_shield_saver_and_2_kill_chance():
    return play(2, True, True, .02)


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
    num_for_perfect = "inf" if odds == 0 else round(1.0 // odds)

    return TestResult(name, odds * 100, num_for_perfect, round(avg_prizes, 2))


def run_test_suite(num_trials=1_000_000):
    tests = {
        # "No Bonuses": play_with_no_bonuses,
        # "1x Shield": play_with_1x_shield,
        # "1x Shield + Saver": play_with_1x_shield_and_saver,
        # "2x Shield + Saver": play_with_2x_shield_and_saver,
        # "2x Shield + Saver + X2": play_with_2x_shield_saver_and_x2,
        "2x Shield + Saver + X2 + 1% Kill Chance: wait strategy(inf)": play_wait_strategy_with_2x_shield_saver_x2_and_1_kill_chance,
        # "2x Shield + Saver + X2 + 1% Kill Chance: wait strategy(1)": play_wait_strategy_with_2x_shield_saver_x2_and_1_kill_chance_wait_1,
        # "2x Shield + Saver + X2 + 1% Kill Chance: wait strategy(2)": play_wait_strategy_with_2x_shield_saver_x2_and_1_kill_chance_wait_2,
        # "2x Shield + Saver + X2 + 1% Kill Chance: wait strategy(3)": play_wait_strategy_with_2x_shield_saver_x2_and_1_kill_chance_wait_3,
        "2x Shield + Saver + X2 + 1% Kill Chance": play_with_2x_shield_saver_and_1_kill_chance,
        "2x Shield + Saver + X2 + 2% Kill Chance": play_with_2x_shield_saver_and_2_kill_chance
    }
    results = []
    tests_run = 0
    for name, test_func in tests.items():
        result = run_test(name, test_func, num_trials)
        results.append(result)
        tests_run += 1
        print(f"Progress: {tests_run} / {len(tests)}")

    table_data = []
    for result in results:
        table_data.append([result.name, result.perfect_percent, result.num_for_perfect, result.avg_num_prizes])

    print(tabulate(table_data, headers=["NAME", "PERFECT %", "HUNTS/PERFECT", "AVG PRIZES"]))


run_test_suite()

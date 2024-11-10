from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
from pynput import keyboard as mainKeyboard
import pyautogui
from enum import Enum
from time import sleep, time
import Quartz


class State(Enum):
    PAUSED = 1
    QUITTING = 2
    RUNNING = 3


mouse = MouseController()
keyboard = KeyboardController()
current_state = State.PAUSED
past_state = State.RUNNING
game_region = ()  # x, y (of top left corner), width, height

# times
jump_time = 0
high_jump_time = 0
dash_time = 0
rage_time = 0
minion_time = 0
check_chest_hunter_time = 0
check_bonus_stage_time = 0

# location offsets
jump_offset = (412, 50)
dash_offset = (93, 585)
rage_offset = (690, 128)
chest_hunter_close_offset = (338, 598)
chest_hunter_border_offset_1 = (3, 33)
chest_hunter_border_offset_2 = (337, 31)
chest_hunter_border_offset_3 = (2, 114)
bonus_stage_border_offset_1 = (259, 196)
bonus_stage_border_offset_2 = (259, 473)
bonus_stage_swipe_left_offsets = [(302, 539), (302, 488)]
bonus_stage_swipe_right_offsets = [(526, 539), (526, 491)]
bonus_stage_close_offset = (472, 492)
bonus_stage_start_offset = (443, 75)
menu_offset = (68, 85)
minion_start_offset = (205, 157)
minion_tab_offset = (208, 600)
menu_close_offset = (361, 604)

# pixel color values
chest_hunter_border_color = (220, 215, 205)
chest_hunter_saver_color = (252, 236, 79)
close_color = (165, 33, 22)  # (140, 28, 19)
# bonus_stage_border_color = (206, 163, 123)
bonus_stage_border_color = (186, 142, 104)
bonus_stage_start_color = (68, 150, 169)

# Intervals (seconds)
jump_int = .08  # 20/second
high_jump_int = 3
dash_int = 3
rage_int = 20
check_bonus_stage_int = 20
check_chest_hunter_int = 20
minion_int = 600  # 10 mins

using_built_in_display = True
chest_hunter_offsets = [
    (145, 265), (223, 265), (301, 265), (380, 265), (458, 265), (534, 265), (611, 265), (687, 265),
    (145, 343), (223, 343), (301, 343), (380, 343), (458, 343), (534, 343), (611, 343), (687, 343),
    (145, 421), (223, 421), (301, 421), (380, 421), (458, 421), (534, 421), (611, 421), (687, 421),
    (223, 500), (301, 500), (380, 500), (458, 500), (534, 500), (611, 500)
]


def listen_to_input():
    listener = mainKeyboard.Listener(on_release=on_release)
    listener.start()


def on_press(key):
    if key == Key.up:
        pyautogui.screenshot(region=game_region).save(f"./recordings/jump-states/{time()}.png")


def on_release(key):
    global current_state, past_state
    if key == Key.space:
        if current_state == State.PAUSED:
            print("Un-pausing game!")
            change_state(past_state)
        else:
            print("Pausing game!")
            change_state(State.PAUSED)
    elif key == Key.esc:
        print("Quitting!")
        change_state(State.QUITTING)


def change_state(new_state):
    global current_state, past_state, game_region
    past_state = current_state
    current_state = new_state
    if past_state is State.PAUSED:
        verify_window()


def click(pos, clicks=1, wait=0.0):
    mouse.position = pos
    mouse.click(button=Button.left, count=clicks)
    if wait > 0:
        sleep(wait)


def find_window(name):
    windows = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
    for window in windows:
        if window.get(Quartz.kCGWindowOwnerName) == name:
            bounds = window.get(Quartz.kCGWindowBounds)
            return int(bounds["X"]), int(bounds["Y"]), int(bounds["Width"]), int(bounds["Height"])

    print(f"Could not find window '{name}'!")
    exit()


def verify_window(name="Idle Slayer", required_dims=(831, 651)):
    global game_region, using_built_in_display
    using_built_in_display = Quartz.CGMainDisplayID() == 1  # I am not sure if this is different for external displays yet
    game_region = find_window(name)
    dims = game_region[2:]
    if dims != required_dims:
        print("Window is not correctly sized!")
        print(f"Current dimensions: {dims}")
        print(f"Expected dimensions: {required_dims}")
        exit()


def offset_to_screen(offset, double=False):
    if double:
        return (game_region[0] + offset[0]) * 2, (game_region[1] + offset[1]) * 2
    else:
        return game_region[0] + offset[0], game_region[1] + offset[1]


def jump():
    click(offset_to_screen(jump_offset))


def high_jump():
    sleep(.5)
    mouse.position = offset_to_screen(jump_offset)
    mouse.press(Button.left)
    sleep(.3)
    mouse.release(Button.left)


def dash():
    sleep(.1)
    click(offset_to_screen(dash_offset), clicks=2)


def rage():
    sleep(.1)
    click(offset_to_screen(rage_offset), clicks=1)


def pixel_color_in_range(pixel_color, expected_color, tolerance=10):
    r, g, b = pixel_color[:3]
    ex_r, ex_g, ex_b = expected_color
    return (abs(r - ex_r) <= tolerance) and (abs(g - ex_g) <= tolerance) and (abs(b - ex_b) <= tolerance)


def check_pixels_match(pix_positions, expected_color, tolerance=10):
    screenshot = pyautogui.screenshot(region=game_region)
    return all(pixel_color_in_range(screenshot.getpixel(pos), expected_color, tolerance) for pos in pix_positions)


def check_chest_hunter():
    return check_pixels_match(
        [chest_hunter_border_offset_1, chest_hunter_border_offset_2, chest_hunter_border_offset_3],
        chest_hunter_border_color, tolerance=30)


def check_chest_hunter_over():
    return check_pixels_match([chest_hunter_close_offset], close_color)


def play_deploy_minions():
    click(offset_to_screen(menu_offset), wait=0.5)
    click(offset_to_screen(menu_offset), wait=0.5)
    click(offset_to_screen(minion_tab_offset), wait=0.5)
    click(offset_to_screen(minion_tab_offset), wait=0.5)
    click(offset_to_screen(minion_start_offset), wait=0.5)
    click(offset_to_screen(minion_start_offset), wait=0.5)
    click(offset_to_screen(minion_start_offset), wait=0.5)
    click(offset_to_screen(minion_start_offset), wait=0.5)
    click(offset_to_screen(menu_close_offset), wait=0.5)
    click(offset_to_screen(menu_close_offset), wait=0.5)


def play_chest_hunter():
    sleep(3)  # gives time for saver to be located
    num_chests_opened = 0
    while not check_chest_hunter_over() and current_state is State.RUNNING:
        for pos in chest_hunter_offsets:
            click(offset_to_screen(pos))
            num_chests_opened += 1
            sleep(1.5)
            if check_chest_hunter_over() or current_state is not State.RUNNING:
                break
            if num_chests_opened == 2:
                screenshot = pyautogui.screenshot(region=game_region)
                saver_location = None
                for i, pix in enumerate(screenshot.getdata()):
                    if pix[1] > 100 and pix[:3] == chest_hunter_saver_color:
                        saver_location = (i % game_region[2]) + 10, (i // game_region[2]) + 10
                        break
                if saver_location is not None:
                    sleep(2)
                    click(offset_to_screen(saver_location), clicks=1)
                    click(offset_to_screen(saver_location), clicks=1)

    # pyautogui.screenshot(region=game_region).save(f"/Users/jacobwilliams/dev/IdleSlayer/recordings/chest-hunt-results/{time()}.png")

    while check_chest_hunter_over() and current_state is State.RUNNING:
        click(offset_to_screen(chest_hunter_close_offset), clicks=2)


def check_bonus_stage():
    return check_pixels_match([bonus_stage_border_offset_1, bonus_stage_border_offset_2], bonus_stage_border_color)


def clear_box():
    for i in range(2):
        sleep(.25)
        mouse.position = offset_to_screen(bonus_stage_swipe_left_offsets[i])
        mouse.press(Button.left)
        sleep(.25)
        mouse.move(277, 0)
        sleep(.25)
        mouse.release(Button.left)
        sleep(.25)

        if not check_bonus_stage():
            break

        mouse.position = offset_to_screen(bonus_stage_swipe_right_offsets[i])
        mouse.press(Button.left)
        sleep(.25)
        mouse.move(-277, 0)
        sleep(.25)
        mouse.release(Button.left)
        sleep(.25)

        if not check_bonus_stage():
            break


def play_bonus_stage():
    clear_box()
    while check_bonus_stage() and current_state is State.RUNNING:
        clear_box()

    sleep(50)
    click(offset_to_screen(bonus_stage_close_offset))
    sleep(1)
    click(offset_to_screen(bonus_stage_close_offset))
    sleep(1)
    click(offset_to_screen(bonus_stage_close_offset))


def play_bonus_stage_improved_v2():
    clear_box()
    while check_bonus_stage() and current_state is State.RUNNING:
        clear_box()
    start_time = time()
    jump_time = 0
    jump_int = .75
    while current_state is State.RUNNING and time() - start_time < 300:
        screenshot = pyautogui.screenshot(region=game_region)
        if pixel_color_in_range(screenshot.getpixel(bonus_stage_close_offset), close_color):
            while pixel_color_in_range(screenshot.getpixel(bonus_stage_close_offset), close_color):
                click(offset_to_screen(bonus_stage_close_offset), clicks=2)
                sleep(1)
                screenshot = pyautogui.screenshot(region=game_region)
            break

        if time() - jump_time > jump_int:
            click(offset_to_screen(dash_offset))


def play():
    global current_state, game_region, jump_time, dash_time, rage_time, check_chest_hunter_time, check_bonus_stage_time, high_jump_time, minion_time

    listen_to_input()
    verify_window()
    print(f"Game Paused!!")
    while current_state is not State.QUITTING:
        if current_state is not State.PAUSED:
            # pos_x, pos_y = mouse.position
            # pixel_pos = pos_x, pos_y
            # if using_built_in_display:
            #     pixel_pos = pos_x * 2, pos_y * 2
            # print(f"Mouse: X={pos_x - game_region[0]}, Y={pos_y - game_region[1]} Color: {pyautogui.pixel(*pixel_pos)}")
            # sleep(1)

            t = time()
            if t - jump_time > jump_int:
                jump()
                jump_time = t
            if t - high_jump_time > high_jump_int:
                high_jump()
                high_jump_time = t
            if t - dash_time > dash_int:
                dash()
                dash_time = t
            if t - rage_time > rage_int:
                rage()
                rage_time = t
            if t - check_bonus_stage_time > check_bonus_stage_int:
                if check_bonus_stage():
                    # exit()
                    play_bonus_stage_improved_v2()
                check_bonus_stage_time = t
            if t - check_chest_hunter_time > check_chest_hunter_int:
                if check_chest_hunter():
                    play_chest_hunter()
                check_chest_hunter_time = t
            if t - minion_time > minion_int:
                play_deploy_minions()
                minion_time = t


play()

# sleep(2)
# verify_window()
# listen_to_input()
# current_state = State.RUNNING
# play_bonus_stage_improved_v2()

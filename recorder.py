from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
from pynput import keyboard as mainKeyboard
import pyautogui
from time import time, sleep
import Quartz

mouse = MouseController()
keyboard = KeyboardController()
game_region = ()
using_built_in_display = False


def on_press(key):
    global current_action_start_time, running, key_pressed
    if key == Key.space:
        running = False
    elif not key_pressed:
        key_pressed = True
        current_action_start_time = time()


def on_release(key):
    global current_action_start_time, running, key_pressed
    if key == Key.space:
        running = False
    else:
        key_pressed = False
        t = time()
        action = Action(current_action_start_time - recording_start_time, t - current_action_start_time)
        print(action)


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


def pixel_color_in_range(pixel_color, expected_color, tolerance=10):
    r, g, b = pixel_color
    ex_r, ex_g, ex_b = expected_color
    return (abs(r - ex_r) <= tolerance) and (abs(g - ex_g) <= tolerance) and (abs(b - ex_b) <= tolerance)


def check_pixels_match(offset_positions, expected_color, tolerance=10):
    screenshot = pyautogui.screenshot(region=game_region)
    return all(pixel_color_in_range(screenshot.getpixel(pos)[:3], expected_color, tolerance) for pos in offset_positions)


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


verify_window()
listener = mainKeyboard.Listener(on_release=on_release, on_press=on_press)
listener.start()

started = False
print("Recording...")
while running:
    # pos_x, pos_y = mouse.position
    # pixel_pos = pos_x * 2, pos_y * 2
    # print(f"Mouse: X={pos_x - game_region[0]}, Y={pos_y - game_region[1]} Color: {pyautogui.pixel(*pixel_pos)}")
    # sleep(.5)

    # pos = offset_to_screen((443, 75), double=using_built_in_display)
    # screenshot = pyautogui.screenshot()
    # if not started and pixel_color_in_range(screenshot.getpixel(pos)[:3], (68, 150, 169)):
    #     started = True
    #     print("Starting run...")
    #     recording_start_time = time()

    # while check_bonus_stage() and running and not started:
    #     clear_box()
    #     if not check_bonus_stage():
    #         started = True
    #         print("Starting run...")
    #         recording_start_time = time()

    screenshot = pyautogui.screenshot(region=game_region)
    screenshot.save(f"./recordings/stage-2/{time()}.png")






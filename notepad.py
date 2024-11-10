# def play_bonus_stage_improved_v1():
#     # clear_box()
#     # while check_bonus_stage() and current_state is State.RUNNING:
#     #     clear_box()
#
#     # positions
#     bonus_stage_obstacle_positions = [(170, 410), (240, 410)]
#     bonus_stage_roof_position = (70, 200)
#     bonus_stage_hole_position = (180, 475)
#     # colors
#     bonus_stage_sky_colors = [(47, 39, 201), (150, 148, 226), (63, 59, 205), (102, 100, 215), (208, 144, 239)]
#     bonus_stage_ground_colors = [(115, 71, 75), (228, 165, 107), (158, 148, 143)]
#
#     while current_state is State.RUNNING:
#         screenshot = pyautogui.screenshot(region=game_region)
#         # screenshot = Image.open("recordings/stage-2/1718468407.384989.png")
#         # if pixel_color_in_range(screenshot.getpixel(bonus_stage_close_offset), close_color):
#         #     while pixel_color_in_range(screenshot.getpixel(bonus_stage_close_offset), close_color):
#         #         click(offset_to_screen(bonus_stage_close_offset), clicks=2)
#         #         sleep(1)
#         #         screenshot = pyautogui.screenshot(region=game_region)
#         #     break
#
#         hole_found = True
#         hole_pix = screenshot.getpixel(bonus_stage_hole_position)
#         for color in bonus_stage_ground_colors:
#             if pixel_color_in_range(hole_pix, color):
#                 hole_found = False
#                 break
#         if hole_found:
#             print(f"Hole: {hole_pix}")
#
#         roof_found = False
#         roof_pix = screenshot.getpixel(bonus_stage_roof_position)
#         for color in bonus_stage_ground_colors:
#             if pixel_color_in_range(roof_pix, color):
#                 roof_found = True
#                 print("Roof")
#                 break
#
#         for pos in bonus_stage_obstacle_positions:
#             pix = screenshot.getpixel(pos)
#             matches = False
#             for color in bonus_stage_ground_colors:
#                 if pixel_color_in_range(pix, color):
#                     matches = True
#                     break
#             if not matches:
#                 print(f"not obstacle: {pix}")
#             if matches and not roof_found:
#                 print(f"Obstacle: {pix}")
#                 click(offset_to_screen(dash_offset))
#                 # screenshot.save(f"./recordings/test-3/obstacle-{time()}.png")
#         if hole_found:
#             click(offset_to_screen(dash_offset))
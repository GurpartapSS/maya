# from pynput import keyboard

# def on_press(key):
#     try:
#         print('alphanumeric key {0} pressed'.format(
#             key.char))
#     except AttributeError:
#         print('special key {0} pressed'.format(
#             key))

# def on_release(key):
#     print('{0} released'.format(
#         key))
#     if key == keyboard.Key.esc:
#         # Stop listener
#         return False

# # Collect events until released
# with keyboard.Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()

import pygame.joystick as pgJ

pgJ.init()

joysticks = [pgJ.Joystick(x) for x in range(pgJ.get_count())]

print("**** Num ",pgJ.get_count())
if(pgJ.get_count() > 0 ):
    print("**** Is initialised ",joysticks[0].get_init())
    print("**** Name is ",joysticks[0].get_name())
    print("**** Axis # ",joysticks[0].get_numaxes())
    print("**** Buttons # ",joysticks[0].get_numbuttons())
    print("**** Hats # ",joysticks[0].get_numhats())
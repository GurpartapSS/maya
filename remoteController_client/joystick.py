from cv2 import FastFeatureDetector, textureFlattening
import pygame
import botClient

pygame.init()
pygame.joystick.init()

isconnected = False

def get_button(jz):
    global isconnected
    if not isconnected:
        botClient.connection()
        isconnected = True
    DATA_MSG = 0
    for i in range(jz.get_numbuttons()):
        print(f"button {i} value {jz.get_button(i)}")
        DATA_MSG |= (jz.get_button(i) << i)
    print(DATA_MSG)
    botClient.send(str(DATA_MSG))
    if jz.get_button(7) == 1:     
        botClient.disconnect()
        isconnected = False

# -------- Main Program Loop -----------
while True:
    
    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

    # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit this loop.
        elif event.type == pygame.JOYBUTTONDOWN:
            # if not hitin:
            get_button(pygame.joystick.Joystick(i))
            print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            get_button(pygame.joystick.Joystick(i))
            print("Joystick button released.")

pygame.quit()
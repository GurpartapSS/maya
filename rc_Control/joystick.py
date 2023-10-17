import pygame
import botClient as bc
import time

pygame.init()
pygame.joystick.init()

isconnected = False

def get_button(jz):

    DATA_MSG = 0
    for i, val in enumerate(jz):
        print(f"button {i} value {val}")
        DATA_MSG |= (val << i)
    print(DATA_MSG)

    global isconnected
    if not isconnected and (DATA_MSG != 0):
        global rc
        rc = bc.remoteclient()
        rc.connection()
        isconnected = True
    
    if isconnected:
        rc.send(str(DATA_MSG))
        time.sleep(.3)
    
    if jz[7] == 1:     
        rc.disconnection()
        del rc
        isconnected = False
        # sys.exit()

# -------- Main Program Loop -----------
if __name__ == "__main__":
    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        axes = joystick.get_numaxes()

    try:
        while True:
            pygame.event.get()  # Get the latest events from Pygame
            button_state = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]

            # Loop through each button
            if any(button_state):  # If button is pressed
                # print(f"Button {button_state} is pressed")
                get_button(button_state)
                time.sleep(0.1)  # Add a delay to control the rate of sending the button value
    finally:
        # Clean up the joystick and Pygame
        pygame.joystick.quit()
        pygame.quit()
import pygame
import botClient as bc
import time

pygame.init()
pygame.joystick.init()

isconnected = False

def get_button(jz, ht):

    DATA_MSG = 0
    for i, val in enumerate(jz):
        # print(f"button {i} value {val}")
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
    
    if jz[11] == 1:     
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
            hat_state = [list(joystick.get_hat(0)) for i in range(joystick.get_numhats())]
            # for i in hat_state:
            #     button_state.extend(i)
            # Loop through each button
            hat_state = hat_state[0]
            button_coded = []
            if hat_state == None:
                print("Error reading hat state")
                button_coded = [0,0,0,0]
            for val in hat_state:
                    button_coded.append(1 if val == 1 else 0)
                    button_coded.append(1 if val == -1 else 0)
            button_coded.extend(button_state)
            if(any(button_coded)):  # If button is pressed
                # get_button(button_state[:10],hat_state)
                print(f"{button_coded}")
                get_button(button_coded)
                time.sleep(0.1)  # Add a delay to control the rate of sending the button value
    finally:
        # Clean up the joystick and Pygame
        pygame.joystick.quit()
        pygame.quit()
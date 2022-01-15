import pygame
import botClient as bc

pygame.init()
pygame.joystick.init()

isconnected = False

def get_button(jz):

    DATA_MSG = 0
    for i in range(jz.get_numbuttons()):
        print(f"button {i} value {jz.get_button(i)}")
        DATA_MSG |= (jz.get_button(i) << i)
    print(DATA_MSG)

    global isconnected
    if not isconnected and (DATA_MSG != 0):
        global rc
        rc = bc.remoteclient()
        rc.connection()
        isconnected = True
    
    if isconnected:
        rc.send(str(DATA_MSG))
    
    if jz.get_button(7) == 1:     
        rc.disconnection()
        del rc
        isconnected = False
        # sys.exit()

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
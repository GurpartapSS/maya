import pygame
import autoBot.remoteController_client.botClient as botClient
# Initialize the joysticks.
pygame.init()
pygame.joystick.init()

# -------- Main Program Loop -----------
while True:
    # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit this loop.
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
            botClient.connection()
            botClient.disconnect()
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        

pygame.quit()
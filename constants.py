
class joystickConstant:
        BUTTON_DISC     = 7
        BUTTON_ACC      = BUTTON_DISC - 0
        BUTTON_ROTR     = BUTTON_DISC - 1
        BUTTON_REV      = BUTTON_DISC - 2
        BUTTON_ROTL     = BUTTON_DISC - 3
        BUTTON_LEFT     = BUTTON_DISC - 4
        BUTTON_RIGHT    = BUTTON_DISC - 5
        BUTTON_RIGHT_UP = BUTTON_DISC - 6

class networkConstant:
    MSG_FORMAT = 64 #fixing msg length
    PORT = 5000
    FORMAT = 'utf-8'
    DISCONNECT_MSG = "!Disconnect"
    SERVER = '10.0.0.203'

project outline


while true:

    voice recognition -- set automatic/ manual mode (const in background)

    if manual mode:

        motor controlled by joystick 
        if no joystick detected -- error and move back to automatic

    if automatic mode --
        camera ON (const in background)

        movement on audio
        tracking on
            if tracking off -- will not follow face/ person


for "Not running on RPI!" https://github.com/gpiozero/gpiozero/issues/837
sudo chmod og+rwx /dev/gpio*
or 
sudo chown root:$USER /dev/gpiomem
sudo chmod g+rw /dev/gpiomem


To get list of camera devices use:
v4l2-ctl --list-devices

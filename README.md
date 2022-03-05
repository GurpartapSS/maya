project outline


while true:

    voice recognition -- set automatic/ manual mode (const in background)

    Need something that can detect offline and use various keywords
    1. Tflite model to detect Keyword 
    2. https://www.seeedstudio.com/blog/2020/01/23/offline-speech-recognition-on-raspberry-pi-4-with-respeaker/
        Models can be Downloaded from : https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3
        For Queries, check: https://discourse.mozilla.org/

    3. Use coral library -- https://github.com/google-coral/project-keyword-spotter

    To get device index:
    import sounddevice as sd
    print(sd.query_devices()) 

    or 

    cat /proc/asound/cards

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


faces: https://github.com/ibaiGorordo/BlazeFace-TFLite-Inference/blob/f43d126b06fffafb700113820dfa1618635a8f28/BlazeFaceDetection/blazeFaceDetector.py#L151

common problem for python lib conflict in venv:

https://www.py4u.net/discuss/140092

Issue: Failed to load delegate from libedgetpu.so.1


Issue: server.bind(ADDR)
    OSError: [Errno 98] Address already in use
Port is already allocated
Solution:
netstat -tulpn
kill <pid>
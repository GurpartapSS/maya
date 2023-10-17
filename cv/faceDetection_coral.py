# All Models available @ https://coral.ai/models/all/

import time
import cv2
import tflite_runtime.interpreter as tflite
import numpy as np
from camListener import cam_motor

class faceCoral:
    def __init__(self):
        # self.interpreter = tflite.Interpreter("Models/face-detector-quantized_edgetpu.tflite",experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
        self.interpreter = tflite.Interpreter("Models/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite",experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details() #list of input details -- expected size of input
        self.output_details = self.interpreter.get_output_details() #list of output details -- Index #0 Boxes #1 Categories #2 Scores
        self.scoreTHreshold = 0.7
        self.motorStep = 64
        self.moving = 0
        self.motor = cam_motor()
        self.motor.setup()


    def detectFace_AND_apply_boundingBox(self):
        if self.moving > 3:
            self.moving = self.moving + 1
        elif self.moving == 20:
            self.moving = 0
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            self._inpH = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self._inpW = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            # print(self._inpH, self._inpW)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img,(320,320))
            input_data = np.expand_dims(img, axis=0)
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            boxes = np.squeeze(self.interpreter.get_tensor(self.output_details[0]['index']))
            scores = np.squeeze(self.interpreter.get_tensor(self.output_details[2]['index']))
            for i in range(len(scores)):
                if (scores[i] > self.scoreTHreshold) and (scores[i] < 1.0):
                    ymin = int(max(1,(boxes[i][0] * self._inpH)))
                    xmin = int(max(1,(boxes[i][1] * self._inpW)))
                    ymax = int(min(self._inpH,(boxes[i][2] * self._inpH)))
                    xmax = int(min(self._inpW,(boxes[i][3] * self._inpW)))
                    # print(ymin, xmin, ymax, xmax)
                    face_coord = [ymin, xmin, ymax, xmax]
                    self.detect_movement(face_coord)
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

            cv2.imshow('image',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    def detect_movement(self, coord):
        center_W = (coord[1]+coord[3])//2
        motion_ang = abs(self._inpW/2 - center_W) // (self.motorStep *2)
        if motion_ang != 0:
            print("face on sides for times .. ",self.moving)
            if self.moving < 3:
                self.moving = self.moving + 1
                return
            elif self.moving == 3:
                self.moving = self.moving + 1
                print("Moving.. ",motion_ang, " center at..",center_W)
                if(center_W < (self._inpW/2) - 2*self.motorStep):
                    print("Moving left")
                    print(coord[1], self._inpW/4)
                    angle = 1
                    self.motor.rotate(angle)
                elif(center_W > (self._inpW/2) + 2*self.motorStep):
                    print("Moving right")
                    print(coord[3], self._inpW*3/4)
                    angle = -1
                    self.motor.rotate(angle)
        else:
            self.moving = 0


if __name__ == '__main__':
    f = faceCoral()
    f.detectFace_AND_apply_boundingBox()

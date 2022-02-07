# All Models available @ https://coral.ai/models/all/

import cv2
import tflite_runtime.interpreter as tflite
import numpy as np

class faceCoral:
    def __init__(self):
        # self.interpreter = tflite.Interpreter("Models/face-detector-quantized_edgetpu.tflite",experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
        self.interpreter = tflite.Interpreter("Models/ssd_mobilenet_v2_face_quant_postprocess_edgetpu.tflite",experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details() #list of input details -- expected size of input
        self.output_details = self.interpreter.get_output_details() #list of output details -- Index #0 Boxes #1 Categories #2 Scores
        self.scoreTHreshold = 0.7


    def detectFace_AND_apply_boundingBox(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            inpH = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            inpW = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img,(320,320))
            input_data = np.expand_dims(img, axis=0)
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            boxes = np.squeeze(self.interpreter.get_tensor(self.output_details[0]['index']))
            scores = np.squeeze(self.interpreter.get_tensor(self.output_details[2]['index']))
            for i in range(len(scores)):
                if (scores[i] > self.scoreTHreshold) and (scores[i] < 1.0):
                    ymin = int(max(1,(boxes[i][0] * inpH)))
                    xmin = int(max(1,(boxes[i][1] * inpW)))
                    ymax = int(min(inpH,(boxes[i][2] * inpH)))
                    xmax = int(min(inpW,(boxes[i][3] * inpW)))
                    print(ymin, xmin, ymax, xmax)
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

            cv2.imshow('image',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == '__main__':
    f = faceCoral()
    f.detectFace_AND_apply_boundingBox()

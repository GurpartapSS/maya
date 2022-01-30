import cv2
import tflite_runtime.interpreter as tflite
import numpy as np

class faceCoral:
    def __init__(self):
        self.interpreter = tflite.Interpreter("face-detector-quantized_edgetpu.tflite",experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details() #list of details
        self.output_details = self.interpreter.get_output_details() #list of details
        self.scoreTHreshold = 0.7

        self.sigmoidScoreThreshold = np.log(self.scoreTHreshold/(1-self.scoreTHreshold))


    def main(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
        #    img = frame
            inpH = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            inpW = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img,(128,128))
            # print(img.shape)
            input_data = np.expand_dims(img, axis=0)
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            # signatures = interpreter.get_signature_list()
            # print(signatures)
            # interpreter.get_tensor(output['index']).shape
            boxes = np.squeeze(self.interpreter.get_tensor(self.output_details[0]['index']))
            scores = np.squeeze(self.interpreter.get_tensor(self.output_details[1]['index']))
            facesReq = np.where(scores > self.sigmoidScoreThreshold)[0]
            newScores = 1.0/(1.0 + np.exp(-scores[facesReq]))
            for i in range(len(scores)):
                if (scores[i] > self.scoreTHreshold) and (scores[i] < 1.0):
                    ymin = int(max(1,(boxes[i][0] * 300)))
                    xmin = int(max(1,(boxes[i][1] * 300)))
                    ymax = int(min(inpH,(boxes[i][2] * 300)))
                    xmax = int(min(inpW,(boxes[i][3] * 300)))
                    print(ymin, xmin, ymax, xmax)
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

            # Extract inform /ation of filtered detections
            # boxes, keypoints = extractDetections(output0, goodDetectionsIndices)

            # Filter results with non-maximum suppression
            # detectionResults = filterWithNonMaxSupression(boxes, keypoints, scores)
            cv2.imshow('image',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == '__main__':
    f = faceCoral()
    f.main()

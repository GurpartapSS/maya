import cv2
import tflite_runtime.interpreter as tflite
import numpy as np

interpreter = tflite.Interpreter("face-detector-quantized_edgetpu.tflite",experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
interpreter.allocate_tensors()
input_details = interpreter.get_input_details() #list of details
output_details = interpreter.get_output_details() #list of details
# print(output_details)
scoreTHreshold = 0.7

sigmoidScoreThreshold = np.log(scoreTHreshold/(1-scoreTHreshold))

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
    #    img = frame
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img,(128,128))
        # print(img.shape)
        input_data = np.expand_dims(img, axis=0)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        # signatures = interpreter.get_signature_list()
        # print(signatures)
        # interpreter.get_tensor(output['index']).shape
        boxes = np.squeeze(interpreter.get_tensor(output_details[0]['index']))
        scores = np.squeeze(interpreter.get_tensor(output_details[1]['index']))
        facesReq = np.where(scores > sigmoidScoreThreshold)[0]
        newScores = 1.0/(1.0 + np.exp(-scores[facesReq]))
        # print(boxes)

        # Extract information of filtered detections
		boxes, keypoints = extractDetections(output0, goodDetectionsIndices)

		# Filter results with non-maximum suppression
		detectionResults = filterWithNonMaxSupression(boxes, keypoints, scores)

        cv2.imshow('image',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()

import deepspeech
import pyaudio
import numpy as np
from halo import Halo
from audio_tools import VADAudio

Model_path = 'Models/deepspeech-0.9.2-models.tflite'
# scorer_path = 'Models/deepspeech-0.9.3-models.scorer'
model = deepspeech.Model(Model_path)
# model.enableExternalScorer(scorer_path=scorer_path)
# model.beamWidth = 500

import matplotlib.pyplot as plt 

def plotAudio2(output):
        fig, ax = plt.subplots(nrows=1,ncols=1, figsize=(20,4))
        plt.plot(output, color='blue')
        ax.set_xlim((0, len(output)))
        plt.show()

st = model.createStream()
speech = ''
# To handle stream data
def callback(in_data, frame_count, time_info, status):
    global speech
    data = np.frombuffer(in_data,np.int16)
    st.feedAudioContent(data)


Rate = 16000
Chunk_size = 1024
channels  = 1

pa = pyaudio.PyAudio()

stream = None
frames = []
try:
    stream = pa.open(format = pyaudio.paInt16,
    channels=channels,rate=Rate,
    frames_per_buffer=Chunk_size,input=True)
    # stream_callback=callback)
    print("Listening ..")
    while(True):
        data = stream.read(Chunk_size)
        frames.append(np.frombuffer(data,dtype=np.int16))
except KeyboardInterrupt:
    print("Stopping ..")

stream.close()

spinner = Halo('Loading ..')
for frame in frames:
    if spinner: spinner.start()
    st.feedAudioContent(frame)
    # print(st.intermediateDecode())

text = st.finishStream()
spinner.succeed(text)

print("Detected ",text)

if stream is not None:
    stream.close()

# plotAudio2(frames)
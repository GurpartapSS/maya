import deepspeech
import pyaudio
import numpy as np
from halo import Halo
Model_path = 'Models/deepspeech-0.9.3-models.tflite'
# scorer_path = 'Models/deepspeech-0.9.3-models.scorer'
f = deepspeech.Model(Model_path)
# f.enableExternalScorer(scorer_path=scorer_path)

Rate = 16000
Chunk_size = 1024

pa = pyaudio.PyAudio()

stream = None
frames = []
try:
    stream = pa.open(format = pyaudio.paInt16,channels=1,rate=Rate,frames_per_buffer=Chunk_size,input=True)
    print("Listening ..")
    while(True):
        data = stream.read(Chunk_size)
        frames.append(np.frombuffer(data,dtype=np.int16))
except KeyboardInterrupt:
    print("Stopping ..")

stream.close()

spinner = Halo('Loading ..')
st = f.createStream()
for frame in frames:
    if spinner: spinner.start()
    st.feedAudioContent(frame)

text = st.finishStream()
spinner.succeed(text)

# print("Detected ",text)

if stream is not None:
    stream.close()
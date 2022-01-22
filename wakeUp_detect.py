#
# Copyright 2018 Picovoice Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from sqlite3 import adapt
import pvporcupine as pvp
import pyaudio
import struct
import traceback

from pygame import K_y

class AudioDetection:

    def __init__(self):
        self.__num_keywords = 1
        self.__keyword = 'sheldon'
        self.__model_path = pvp.MODEL_PATH
        self.__key_access = ''
        self.__keyword_path = ['Models/sheldon_en_raspberry-pi_v2_1_0.ppn']
        self.__input_device_index = 2
        self.__lib_path = pvp.LIBRARY_PATH
        self.__sample_format = pyaudio.paInt16
        self.__channels = 1

    def getKeyword(self):
        print(f'listening for: {self.__keyword}')

        pa = None
        stream = None
        porcupine = None

        try:
            porcupine = pvp.Porcupine(self.__key_access,
            library_path=self.__lib_path,
            model_path=self.__model_path,
            keyword_paths=self.__keyword_path,
            sensitivities=[0.5]*len(self.__keyword_path))
            pa = pyaudio.PyAudio()

            stream = pa.open(format=self.__sample_format,
                channels=self.__channels,
                rate=porcupine.sample_rate,
                frames_per_buffer=porcupine.frame_length,
                input=True)
            print("Listening ...")

            while(True):
    
                pcm = stream.read(porcupine.frame_length)

                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                
                result = porcupine.process(pcm)

                if(result >= 0):
                    print(f"{self.__keyword} Detected!")
                    stream.close()
                    print("Stream Closed..")
                    break
        
        except KeyboardInterrupt:
            print("Interrupted, stopping ..")

        except:
            print(traceback.format_exc())
        
        finally:
            if porcupine is not None:
                porcupine.delete()

            if pa is not None:
                pa.terminate()
            
            if stream is not None:
                stream.close()

# Test
# if __name__ == '__main__':
#     ad = AudioDetection()
#     ad.getKeyword()
#     del ad


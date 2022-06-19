# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Runs a model on the edgetpu.

Useage:
python3 run_model.py --model_file model_edgetpu.tflite
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

from click import command
import model
import numpy as np
sys.path.append('../')
import socket


class sendHotWheels:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)
        self.host = socket.gethostname() # or just use (host = '')
        self.port = 12345
        self.s.connect((self.host, self.port))
    def send(self,data):
        self.s.send(str(data).encode('utf-8')) # msg can only be 1024 bytes long
    def __del__(self):
        self.s.close()
    def run_cmd(self,command):
          print("run run run ")
          self.send(command)

def main():
  parser = argparse.ArgumentParser()
  model.add_model_flags(parser)
  args = parser.parse_args()
  interpreter = model.make_interpreter(args.model_file)
  interpreter.allocate_tensors()
  mic = args.mic if args.mic is None else int(args.mic)
  hw = sendHotWheels()
  # r.run_cmd()
  model.classify_audio(mic, interpreter,
                       labels_file="config/labels_gc2.raw.txt",
                       commands_file="config/commands_v2.txt",
                       dectection_callback=hw.run_cmd,
                       sample_rate_hz=int(args.sample_rate_hz),
                       num_frames_hop=int(args.num_frames_hop))

if __name__ == "__main__":
  main()
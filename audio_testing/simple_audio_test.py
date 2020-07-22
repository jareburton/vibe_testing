#!/usr/bin/env python3

import simpleaudio as sa
import numpy as np
from math import ceil

freq = 120

sample_rate = 44100
duration = 5

print('generating audio')
t = np.linspace(0, duration, ceil(duration*sample_rate), False)

# generate sine wave notes
note = np.sin(freq * t * 2 * np.pi)

audio = np.hstack((note, note, note, note))
audio *= 32767 / np.max(np.abs(audio))
audio = audio.astype(np.int16)

# start playback
print('Playing audio')
play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

# wait for playback to finish before exiting
play_obj.wait_done()
print('done')

#!/usr/bin/env python3

import simpleaudio as sa
import numpy as np
from math import ceil
import argparse

def play_tone(freq, duration, sample_rate=44100):
    print('generating audio {0} hz {1} secs'.format(freq, duration))
    t = np.linspace(0, duration, ceil(duration*sample_rate), False)

    # generate sine wave notes
    note = np.sin(freq * t * 2 * np.pi)

    #audio = np.hstack((note, note, note, note))
    audio = note
    audio *= 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)

    # start playback
    print('playing audio')
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

    # wait for playback to finish before exiting
    play_obj.wait_done()
    print('finished audio playback')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--freq', dest='freq', type=float, required=True, help='sets tone frequency (Hz)')
    parser.add_argument('--dur', dest='duration', type=float, required=True, help='sets tone duration (s)')
    args = parser.parse_args()

    play_tone(args.freq, args.duration)

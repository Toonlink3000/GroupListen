#!/usr/bin/env python3
"""Pass input directly to output.

https://app.assembla.com/spaces/portaudio/git/source/master/test/patest_wire.c

"""
import argparse

import sounddevice as sd
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)
import threading
import sys

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-i', '--input-device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-oa', '--output-device-a', type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    '-ob', '--output-device-b', type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    '-c', '--channels', type=int, default=2,
    help='number of channels')
parser.add_argument('--dtype', help='audio data type')
parser.add_argument('--samplerate', type=float, help='sampling rate')
parser.add_argument('--blocksize', type=int, help='block size')
parser.add_argument('--latency', type=float, help='latency in seconds')
args = parser.parse_args(remaining)


def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

def clone_audio_stream(input_device, output_device, samplerate, blocksize, dtype, latency, channels, callback):
    print("thread started")
    with sd.Stream(device=(input_device, output_device), samplerate=samplerate, blocksize=blocksize, dtype=dtype, latency=latency,channels=channels, callback=callback):
        print("device " + str(output_device) + "Is being output to")
        input()

def main():
    a = threading.Thread(target = clone_audio_stream, args = (args.input_device, args.output_device_a, args.samplerate, args.blocksize, args.dtype, args.latency, args.channels, callback), daemon=True)
    b = threading.Thread(target = clone_audio_stream, args = (args.input_device, args.output_device_b, args.samplerate, args.blocksize, args.dtype, args.latency, args.channels, callback), daemon=True)
    a.start()
    b.start()
    print("press enter to quit")
    input()

if __name__ == "__main__":
    main()
    sys.exit()

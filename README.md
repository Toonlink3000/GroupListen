# GroupListen
Divert audio from one audio device to another on multiple devices at the same time.
## How to run
To duplicate the audio being outputed by programs on your PC use this tool with an audio driver like [VB Cable](https://vb-audio.com/Cable/) for Windows and MacOS.
On Linux you can folow this guide: [Create a Virtual Microphone on Linux with Pulseaudio for Obs Studio](https://www.youtube.com/watch?v=Goeucg7A9qE).
1. Install the dependancies
3. Run `python gui.py`
### Dependancies
The software is only tested with Python 3.10.
The only dependancy is sounddevice which can be installed with the folowing command:
`pip install sounddevice`
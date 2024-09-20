# import pyttsx3 as speaker
# import sys

# text =sys.argv[1]
# print(text)
# tts = speaker.init()

# tts.say("hello there")
# tts.runAndWait()

import sys
import pyttsx3
text =sys.argv[1]
# print(text)

engine = pyttsx3.init()
engine.say(".... text hello there")
engine.runAndWait()
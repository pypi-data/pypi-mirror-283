# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

import colemen_utils as c
import pyttsx3



class TextToSpeech:
    def __init__(self):
        self.rate = 200
        self.volume = 1
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        [print(v.name) for v in voices]
        self.voice_id = 1

    def speak(self,value):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[self.voice_id].id)
        self.engine.setProperty('volume', self.volume)
        self.engine.setProperty('rate', self.rate)
        self.engine.say(value)
        self.engine.runAndWait()
        
    def testicles(self):
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        for voice in voices:
            print(voice)
            engine.setProperty('voice', voice.id)
            engine.say('testicles')
            engine.runAndWait()

if __name__ == '__main__':
    t = TextToSpeech()
    #t.speak("testicles")
    
    t.testicles()
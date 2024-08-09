
# Import the required module
import pyttsx3
import subprocess 
# Create a string
string = "Lorem Ipsum is simply dummy text " \
    + "of the printing and typesetting industry."
 
# Initialize the Pyttsx3 engine
engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
engine.setProperty('rate',80)
#engine.say('Hello my name is Heitor')



# We can use file extension as mp3 and wav, both will work
engine.save_to_file("Sou uma inteligência artificial ", 'speech.mp3')
# Wait until above command is not finished.
engine.runAndWait()

from voxpopuli import Voice
voice = Voice(lang="br", speed=135,volume=2,voice_id=3)

print(Voice.list_voice_ids())

wav = voice.to_audio("Meu nome é Heitor")

with open("salut.wav", "wb") as wavfile:
    wavfile.write(wav)
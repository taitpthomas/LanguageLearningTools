"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
from playsound import playsound
import pyperclip
import keyboard

# hotkey
done = False


def hotkey_callback(arg1, arg2):
    global done
    print("Hello from a function")
    done = True


# add hotkey
keyboard.add_hotkey('ctrl+shift+/', hotkey_callback, args=('triggered', 'hotkey'))
print("waiting or hotkey")
while not done:
    pass

# clipboard
# pyperclip.copy("something")
mytext = pyperclip.paste()
print(mytext)

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text=mytext)

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
# noinspection PyTypeChecker
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')

playsound('output.mp3')

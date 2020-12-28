"""Synthesizes speech from the input string of text or ssml.
Required package:
    pip install --upgrade google-cloud-texttospeech
    pip install keyboard
    pip install playsound
    pip install pyperclip

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
from playsound import playsound
import pyperclip
import keyboard
import os

# Global exit flag
done = False

def hotkey_done():
    global done
    done = True


def hotkey_speak(speak_client, speak_voice, speak_audio_config):
    # speak the data from the clipboard
    mytext = pyperclip.paste()
    if len(mytext) < 500:
        print("Info")

    # synthesize_speech
    response = speak_client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=mytext),
        voice=speak_voice,
        audio_config=speak_audio_config
    )

    # write the response's audio_content binary data to a file
    with open("output.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

    # playsound
    playsound('output.mp3')
    # workaround for playsound not releasing the audio file
    os.remove('output.mp3')


# Instantiates a Text to speech client, create the voice and audio_config
client = texttospeech.TextToSpeechClient()
# noinspection PyTypeChecker
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)
# noinspection PyTypeChecker
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# add hotkey
keyboard.add_hotkey('ctrl+shift+.', hotkey_done)
keyboard.add_hotkey('ctrl+shift+/', hotkey_speak, args=(client, voice, audio_config))

# wait loop
print("waiting for hotkeys:")
print("    ctrl shift / to talk")
print("    ctrl shift . to exit")
while not done:
    pass

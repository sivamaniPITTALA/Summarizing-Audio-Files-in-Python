import os
import threading
import speech_recognition as sr
from summarizer import Summarizer

# Create a recognizer instance
recognizer = sr.Recognizer()

# Create a microphone instance
microphone = sr.Microphone()

# Define the data folder path where you want to save files
data_folder = 'without\\data\\download_from_microphone'

# Create the data folder if it doesn't exist
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Initialize an audio file name and recording state
audio_file_path = None
recording = False

# Define the start and end recording keywords
start_recording_keyword = "start recording"
end_recording_keyword = "end recording"

# Function to start recording
def start_recording():
    global recording, audio_file_path
    print("Recording started.")
    audio_file_path = os.path.join(data_folder, "audio.wav")
    with open(audio_file_path, "wb") as audio_file:
        recording = True
        while recording:
            audio = recognizer.listen(microphone, timeout=None)
            audio_file.write(audio.get_wav_data())

# Function to stop recording
def stop_recording():
    global recording
    recording = False
    print(f"Recording stopped. Audio saved as '{audio_file_path}'.")

# Start listening for commands
print("Listening... Say 'start recording' to begin and 'end recording' to stop.")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)
    while True:
        audio = recognizer.listen(source, timeout=None)
        try:
            recognized_text = recognizer.recognize_sphinx(audio)
            if start_recording_keyword in recognized_text.lower():
                start_recording()
            elif end_recording_keyword in recognized_text.lower():
                stop_recording()
            else:
                pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Could not request results: {e}")

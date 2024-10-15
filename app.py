import assemblyai as aai
import google.generativeai as genai
import PyPDF2
import os
import pygame
import threading
import time
import wave
import pyaudio
import requests
import numpy as np

from dotenv import load_dotenv
load_dotenv()

class AutoAudioRecorder:
    def __init__(self, threshold=300, silence_limit=1.5, silence_threshold=50, chunk_size=1024, sample_rate=44100):
        self.threshold = threshold
        self.silence_limit = silence_limit
        self.silence_threshold = silence_threshold
        self.chunk_size = chunk_size
        self.sample_rate = sample_rate
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.sample_rate,
                                  input=True,
                                  frames_per_buffer=self.chunk_size)

    def is_silent(self, data):
        return max(data) < self.silence_threshold

    def record(self):
        print("Listening for speech...")
        audio_started = False
        audio_buffer = []
        silent_chunks = 0

        while True:
            data = np.frombuffer(self.stream.read(self.chunk_size), dtype=np.int16)

            if not audio_started:
                if max(data) > self.threshold:
                    print("Speech detected, recording...")
                    audio_started = True
                    audio_buffer.append(data)
                continue

            if self.is_silent(data):
                silent_chunks += 1
                if silent_chunks > self.silence_limit * self.sample_rate / self.chunk_size:
                    break
            else:
                silent_chunks = 0

            audio_buffer.append(data)

        print("Finished recording.")
        self.save_audio(audio_buffer)

    def save_audio(self, audio_buffer):
        filename = "user_response.wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.sample_rate)

        audio_bytes = b''.join([data.tobytes() for data in audio_buffer])
        wf.writeframes(audio_bytes)
        wf.close()
        print("Audio saved as {}".format(filename))

    def run(self):
        self.record()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

class IGNUS_Assistant:
    def __init__(self, info_path):
        self.aai_api_key = os.getenv("ASSEMBLY_AI_KEY")
        self.gemini_api_key = os.getenv("GEMINAI_API_KEY")
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.elevenlabs_voice_id = "zFLlkq72ysbq1TWC0Mlx"  # Replace with your chosen voice ID

        aai.settings.api_key = self.aai_api_key
        genai.configure(api_key=self.gemini_api_key)

        self.fest_info = self.load_info(info_path)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.chat = self.model.start_chat(history=[])

        system_prompt = f"""You are a public relations representative for IIT Jodhpur's cultural fest, Ignus. Your primary objective is to inform individuals about the fest and assess their interest in purchasing tickets by talking with them such that you are on a call.
        
        Key Instructions:
        Use only this information provided about the fest: {self.fest_info}.
        Avoid using any external information or personal opinions.
        Do not use emojis or stickers to ensure clear audio transcription in the call.
        Maintain a polite, enthusiastic, and concise tone throughout the conversation.
        Try to talk as minimum as possible.
        Engage in a smooth and natural dialogue, asking open-ended questions to gauge interest.
        While returning the term IGNUS return it in "Ignus" term.
        
        Conversation Flow:
        
        Introduction:
        Greet the user warmly and introduce yourself as a representative of IGNUS.
        
        Information Sharing:
        Briefly outline what IGNUS is, highlighting its unique features, such as:
        Diverse cultural events and competitions.
        Participation of renowned artists and performers.
        Opportunities for social awareness through various activities.
        
        Engagement Questions:
        Ask if they have heard about IGNUS before.
        Inquire about their interests in cultural events or specific activities offered at the fest.
        
        Interest Assessment:
        Conclude by asking if they would be interested in purchasing tickets for the fest.
        
        Closing:
        Thank them for their time, regardless of their interest level by saying "Thanks for your time! Hope to see you at the fest. Feel free to reach out with any questions!".
        Remember to keep the conversation flowing naturally while adhering strictly to these guidelines.
        
        Incase: If you think user donot want to talk or they are busy at this moment or they have finished talking to you i.e. they are saying bye or related terms just thank them for their time, regardless of their interest level by saying "Thanks for your time! Hope to see you at the fest. Feel free to reach out with any questions!"
        """

        self.chat.send_message(system_prompt)

        # Initialize pygame mixer for audio
        pygame.mixer.init()
        self.audio_playing = False
        self.audio_thread = None

    def load_info(self, file_path):
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() == '.pdf':
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return ' '.join(page.extract_text() for page in pdf_reader.pages)
        else:
            with open(file_path, 'r') as file:
                return file.read()

    def transcribe_file(self, file_path):
        config = aai.TranscriptionConfig(language_code="en")
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path)
        return transcript.text

    def generate_ai_response(self, user_input):
        response = self.chat.send_message(user_input)
        ai_response = response.text

        print(f"AI: {ai_response}")
        self.generate_audio(ai_response)
        return ai_response


    def generate_audio(self, text):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.elevenlabs_voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.elevenlabs_api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            with open("response.mp3", "wb") as f:
                f.write(response.content)
            
            # Play audio in a separate thread
            self.audio_thread = threading.Thread(target=self.play_audio)
            self.audio_thread.start()
        else:
            print(f"Error generating audio: {response.status_code}")
            print(response.text)

    def play_audio(self):
        self.audio_playing = True
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() and self.audio_playing:
            pygame.time.Clock().tick(10)
        pygame.mixer.music.stop()
        
        # Delete the audio file after playing
        pygame.mixer.music.unload()
        try:
            os.remove("response.mp3")
        except PermissionError:
            print("Couldn't delete response.mp3 immediately. Will try again later.")

    def stop_audio(self):
        self.audio_playing = False
        if self.audio_thread:
            self.audio_thread.join()
        
        # Try to delete the file again if it wasn't deleted after playing
        try:
            if os.path.exists("response.mp3"):
                os.remove("response.mp3")
        except PermissionError:
            print("Couldn't delete response.mp3. Please delete it manually if it persists.")

    def generate_summary(self):
        summary_prompt = """Based on the conversation, do you think the person is interested in buying tickets for IGNUS?
        Respond with 'Yes' if interested, 'No' if not interested, or 'Maybe' if unclear.
        Then provide a brief explanation for your decision."""

        response = self.chat.send_message(summary_prompt)
        summary = response.text
        interest = summary.split()[0].lower()

        print("\nSummary:")
        print(summary)

        return interest

    def record_audio(self):
        recorder = AutoAudioRecorder()
        recorder.run()
        return 1


def main():
    assistant = IGNUS_Assistant(r"E:\PROJECTS\Calling_Bot\Ignus_database.pdf")

    greeting = "Hello! This is a call from IIT Jodhpur regarding our upcoming cultural fest, Ignus. Do you have a moment to talk about it?"
    assistant.generate_audio(greeting)

    while True:
        print("\nStart Speaking if you want to want to give input or interrupt the call.")
        
        user_input = assistant.record_audio()  # No argument here
        
        # Stop the current audio playback
        if user_input :
            assistant.stop_audio()
            transcription = assistant.transcribe_file("user_response.wav")  # The file name is fixed
            print(f"Transcription: {transcription}")
            ai_response = assistant.generate_ai_response(transcription)

        if "thanks for your time! hope to see you at the fest. feel free to reach out with any questions!" in ai_response.lower():
            break

    interest = assistant.generate_summary()  
    return interest

# Run the main function
if __name__ == "__main__":
    result = main()
    print(f"\nFinal Result: The person is {'interested' if result == 'yes' else 'not interested' if result == 'no' else 'possibly interested'} in buying tickets for IGNUS.")

    if result == 'yes':
        print("AI: Someone from our team will contact you in the upcoming days for further process.")
        assistant = IGNUS_Assistant("dummy_path")  # Create a dummy instance just for audio
        assistant.generate_audio("Someone from our team will contact you in the upcoming days for further process.")
        time.sleep(5)  # Give some time for the last audio to play
        assistant.stop_audio()

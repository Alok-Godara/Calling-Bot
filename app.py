import assemblyai as aai
import google.generativeai as genai
import PyPDF2
import os
import pygame
import threading
import time
import wave
import pyaudio
import numpy as np
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime
from gtts import gTTS  # Import gTTS
from pydub import AudioSegment
from pydub.playback import play

from dotenv import load_dotenv
load_dotenv()


#----------------------------------------------------------------------------------------------------------------------------------------------

class ConversationLogger:
    def __init__(self, username):
        self.username = username
        self.conversation = []
        self.start_time = datetime.now()
        
        # Create logs directory if it doesn't exist
        os.makedirs('conversation_logs', exist_ok=True)
        
        # Generate filename
        date_str = self.start_time.strftime("%Y%m%d_%H%M%S")  # Added time to make filename unique
        self.filename = f"conversation_logs/{self.username}_{date_str}.txt"
        
        # Create the file and write header
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(f"Conversation Log for {username}\n")
            f.write(f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
    
    def add_entry(self, speaker, message):
        """Add a new entry to the conversation log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {speaker}: {message}\n"
        self.conversation.append(entry)
        
        # Immediately write to file for real-time logging
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(entry)
    
    def save_summary(self, interest, reason):
        """Save the conversation summary including all dialogue"""
        with open(self.filename, 'a', encoding='utf-8') as f:
            # Add a separator before the summary
            f.write("\n" + "="*50 + "\n")
            f.write("CONVERSATION SUMMARY\n")
            f.write("="*50 + "\n\n")
            
            # Add conversation statistics
            f.write(f"Date: {self.start_time.strftime('%Y-%m-%d')}\n")
            f.write(f"Start Time: {self.start_time.strftime('%H:%M:%S')}\n")
            f.write(f"End Time: {datetime.now().strftime('%H:%M:%S')}\n")
            f.write(f"Total Messages: {len(self.conversation)}\n")
            f.write(f"Interest Level: {interest}\n")
            f.write(f"Reason: {reason}\n\n")
            
    
    def get_complete_log(self):
        """Return the complete conversation as a string"""
        log = []
        with open(self.filename, 'r', encoding='utf-8') as f:
            log = f.readlines()
        return ''.join(log)
#----------------------------------------------------------------------------------------------------------------------------------------------

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

#----------------------------------------------------------------------------------------------------------------------------------------------

class GoogleSheetsManager:
    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        # Load credentials from service account file
        self.credentials = service_account.Credentials.from_service_account_file(
            r'E:\PROJECTS\Calling_Bot\Condfenditial\ignus-bot-8d4cdf53c2a4.json',  # Replace with your service account key path
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = build('sheets', 'v4', credentials=self.credentials)
        
    def get_next_contact(self):
        """Get the next unprocessed contact from the sheet"""
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range='Sheet1!A2:E'  # Adjusted range to include summary column
        ).execute()
        
        values = result.get('values', [])
        for idx, row in enumerate(values, start=2):  # Start from 2 to account for header row
            if len(row) < 4 or not row[3]:  # Check if status column is empty
                return {
                    'row_number': idx,
                    'name': row[0],
                    'phone': row[1]
                }
        return None

    def update_contact_status(self, row_number, interest, reason):
        """Update the contact's status and reason in the sheet"""
        # Update interest status in column D and reason in column E
        range_name = f'Sheet1!D{row_number}:E{row_number}'
        values = [[interest, reason]]
        
        body = {
            'values': values
        }
        
        try:
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            print(f'Sheet updated: {result.get("updatedCells")} cells updated.')
            return True
        except Exception as e:
            print(f'Error updating sheet: {str(e)}')
            return False

#----------------------------------------------------------------------------------------------------------------------------------------------

class IGNUS_Assistant:
    def __init__(self, info_path, contact_name=""):
        self.aai_api_key = os.getenv("ASSEMBLY_AI_KEY")
        self.gemini_api_key = os.getenv("GEMINAI_API_KEY")

        aai.settings.api_key = self.aai_api_key
        genai.configure(api_key=self.gemini_api_key)

        self.fest_info = self.load_info(info_path)
        self.model = genai.GenerativeModel('gemini-1.5-flash-002')
        self.chat = self.model.start_chat(history=[])
        
        self.contact_name = contact_name
        self.logger = ConversationLogger(contact_name)

        system_prompt = f"""You are a public relations representative for IIT Jodhpur's cultural fest, Ignus. You are talking to {self.contact_name}. Your primary objective is to inform them about the fest and assess their interest in purchasing tickets by talking with them such that you are on a call.
        Just normally talk to the other person rather than giving descriptive text in bracketts explaning yourself.
                
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
        
        Incase: If you think user donot want to talk or they are busy at this moment or they have finished talking to you i.e. they are saying bye or related terms just thank them for their time, regardless of their interest level by just saying "Thanks for your time! Hope to see you at the fest. Feel free to reach out with any questions!" only.
        
        Incase: If User doesnot respond or "no speech detected" messege is sent to you ask the user to say again as you were unable to understand.
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
        """Transcribe audio file and handle empty transcriptions"""
        config = aai.TranscriptionConfig(language_code="en")
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path)
        
        # Handle empty or None transcription
        if not transcript.text or transcript.text.strip() == "":
            return "No speech detected"  # Changed from just "No" for better logging
        return transcript.text

    def generate_ai_response(self, user_input):
        # First, log the user's input if it's not "No speech detected"
        if user_input != "No speech detected":
            self.logger.add_entry("User", user_input)
        
        # Generate and log AI response
        response = self.chat.send_message(user_input)
        ai_response = response.text
        self.logger.add_entry("AI", ai_response)
        
        print(f"AI: {ai_response}")
        self.generate_audio(ai_response)
        return ai_response

    def generate_audio(self, text):
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save the audio file
            tts.save("response.mp3")
            
            # Play audio in a separate thread
            self.audio_thread = threading.Thread(target=self.play_audio)
            self.audio_thread.start()
        except Exception as e:
            print(f"Error generating audio: {str(e)}")


    def play_audio(self, speed=1.2):
        # Load the audio file
        audio = AudioSegment.from_mp3("response.mp3")
        
        # Change the frame rate to adjust speed
        # Note: This will also affect pitch
        faster_audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * speed)
        })
        
        # Play the modified audio
        play(faster_audio)
        
        # Delete the audio file after playing
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
        """Generate a concise summary of the conversation in two steps"""
        # Step 1: Get interest level
        interest_prompt = """Based on our conversation, provide a single word indicating interest level.
        ONLY use: YES, NO, or MAYBE
        
        Format your response exactly like this:
        Interest: [YES/NO/MAYBE]"""
        
        interest_response = self.chat.send_message(interest_prompt)
        interest = interest_response.text.split(':')[1].strip().lower()
        
        # Step 2: Get reason for interest level
        reason_prompt = f"""Based on our conversation and the interest level of {interest.upper()}, 
        provide a brief explanation (max 200 letters) for this interest level.
        Focus on key factors that influenced their decision or interest level.
        
        Format your response exactly like this:
        Reason: [Your 2-3 line explanation]"""
        
        reason_response = self.chat.send_message(reason_prompt)
        reason = reason_response.text.split(':', 1)[1].strip() if ':' in reason_response.text else "No reason provided"
        
        return interest, reason

    def record_audio(self):
        recorder = AutoAudioRecorder()
        recorder.run()
        return 1

#----------------------------------------------------------------------------------------------------------------------------------------------        
        

def main():
    # Initialize the Google Sheets manager
    sheets_manager = GoogleSheetsManager('1FLI34AfrIOnewMRBjXr44NOdOpHm5Z848H4pHLtsFmc')
    
    while True:
        # Get the next contact to process
        contact = sheets_manager.get_next_contact()
        if not contact:
            print("No more contacts to process")
            break
            
        print(f"\nProcessing contact: {contact['name']}")
        
        # Initialize the assistant
        assistant = IGNUS_Assistant(
            r"E:\PROJECTS\Calling_Bot\Ignus_database.pdf",
            contact_name=contact['name']
        )

        # Initial greeting
        greeting = f"Hello {contact['name']}! This is a call from IIT Jodhpur regarding our upcoming cultural fest, Ignus. Do you have a moment to talk about it?"
        assistant.logger.add_entry("AI", greeting)
        assistant.generate_audio(greeting)

        conversation_active = True
        while conversation_active:
            print("\nStart Speaking if you want to give input or interrupt the call.")
            
            user_input = assistant.record_audio()
            
            if user_input:
                assistant.stop_audio()
                transcription = assistant.transcribe_file("user_response.wav")
                
                # Print and log the transcription
                print(f"Transcription: {transcription}")
                
                # Generate and log AI response
                ai_response = assistant.generate_ai_response(transcription)
                
                # Check for conversation end
                if "thanks for your time! hope to see you at the fest. feel free to reach out with any questions!" in ai_response.lower():
                    conversation_active = False

        # Generate and log summary
        interest, reason = assistant.generate_summary()
        interest_value = interest.upper()
        
        # Save conversation summary
        assistant.logger.save_summary(interest_value, reason)
        
        # Update sheet
        sheets_manager.update_contact_status(
            contact['row_number'],
            interest_value,
            reason
        )
        
        # Print final status
        print(f"\nCompleted processing contact: {contact['name']}")
        print(f"Interest: {interest_value}")
        print(f"Reason: {reason}")
        
        print(f"Conversation log saved to: {assistant.logger.filename}")
        
        # Small delay between contacts
        time.sleep(2)

if __name__ == "__main__":
    main()

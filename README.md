# Calling Assistant Bot

## Overview

The Calling Assistant Bot is an automated audio-based conversational assistant designed for IIT Jodhpur's annual cultural fest, **IGNUS**. The bot interacts with potential attendees over audio, providing fest details and gauging interest in ticket purchases. This project incorporates audio recording, transcription, AI-generated responses, and text-to-speech (TTS) capabilities to deliver a smooth user experience.

## Features

- **Audio Recording**: Automatically detects speech and records the user's response.
- **Transcription**: Converts the recorded audio into text using AssemblyAI.
- **AI-Generated Responses**: Uses Google Gemini AI to generate conversational responses based on the user's input.
- **Text-to-Speech**: Converts AI responses into audio using ElevenLabs API.
- **Ticket Purchase Interest Assessment**: Assesses the user's interest in purchasing tickets and provides a summary.

## Requirements

### Libraries

- **AssemblyAI**: For transcribing audio files.
- **Google Generative AI (Gemini)**: For generating conversation responses.
- **PyPDF2**: For reading and extracting fest information from PDFs.
- **Pygame**: For audio playback of responses.
- **Pyaudio**: For capturing and processing live audio from the microphone.
- **Requests**: For interacting with external APIs (like ElevenLabs for TTS).
- **Numpy**: For processing audio data.

### APIs

You will need the following API keys:

- **AssemblyAI API Key** (for transcription): [Get it here](https://www.assemblyai.com/)
- **Google Gemini API Key** (for generative responses): [Get it here](https://developers.generativeai.google/)
- **ElevenLabs API Key** (for text-to-speech): [Get it here](https://beta.elevenlabs.io/)

### Environment Variables

Store your API keys in an `.env` file with the following variables:

```env
ASSEMBLY_AI_KEY=your_assembly_ai_key
GEMINAI_API_KEY=your_google_gemini_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/IGNUS-Assistant-Bot.git
    ```

2. Navigate to the project directory:

    ```bash
    cd IGNUS-Assistant-Bot
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your API keys as shown below:

    ```env
    ASSEMBLY_AI_KEY=your_assembly_ai_key
    GEMINAI_API_KEY=your_google_gemini_key
    ELEVENLABS_API_KEY=your_elevenlabs_key
    ```

## Usage

1. Start the bot by running:

    ```bash
    python ignus_assistant.py
    ```

2. The bot will greet the user and begin the conversation. Follow the on-screen prompts to provide input. 
   The conversation will flow based on the user's responses, and the bot will assess interest in purchasing tickets for IGNUS.

3. The bot automatically stops once the conversation concludes, and it provides a summary of the user's interest.

## How It Works

1. **Conversation**: The bot starts by greeting the user and sharing information about IGNUS based on a provided PDF file. It then asks the user open-ended questions to gauge their interest.

2. **Audio Input**: The user speaks their responses, which are automatically recorded and saved.

3. **Transcription**: The recorded audio is transcribed into text using AssemblyAI.

4. **AI Response Generation**: The transcription is fed into Google Gemini, which generates an appropriate response for the next part of the conversation.

5. **Text-to-Speech**: The generated text is converted into speech using ElevenLabs API, and the audio is played back to the user.

6. **Interest Assessment**: At the end of the conversation, the bot provides a summary indicating whether the user is interested in purchasing tickets.

## Example

Here’s a sample conversation flow:

- Bot: "Hello! This is a call from IIT Jodhpur regarding our upcoming cultural fest, Ignus. Do you have a moment to talk about it?"
- User: "Sure, tell me more."
- Bot: "Ignus is a grand cultural festival with diverse events and performances by renowned artists. Have you attended Ignus before?"
- User: "No, but it sounds interesting!"
- Bot: "Would you like to know more about the events, or are you interested in purchasing tickets?"

At the end, the bot assesses the user's interest and provides a final response.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to get started.

## Acknowledgements

- **AssemblyAI** for transcription services.
- **Google Gemini** for AI response generation.
- **ElevenLabs** for text-to-speech conversion.


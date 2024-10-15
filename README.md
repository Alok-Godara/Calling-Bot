# IGNUS Assistant Bot

## Overview

The IGNUS Assistant Bot is an automated audio-based conversational assistant designed for IIT Jodhpur's annual cultural fest, **IGNUS**. The bot interacts with potential attendees over audio, providing fest details and gauging interest in ticket purchases. This project incorporates audio recording, transcription, AI-generated responses, and text-to-speech (TTS) capabilities to deliver a smooth user experience.

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

### Acknowledgements
AssemblyAI for transcription services.
Google Gemini for AI response generation.
ElevenLabs for text-to-speech conversion.

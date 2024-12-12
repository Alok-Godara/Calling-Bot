# 🎙️ Calling Assistant Bot 📞

Welcome to the **Calling Assistant Bot** project! This is an intelligent, audio-based conversational assistant designed specifically for **IGNUS**, IIT Jodhpur's electrifying annual cultural fest. 🌟

The bot seamlessly interacts with potential attendees over audio, providing details about the fest and gauging their interest in ticket purchases. It's smart, efficient, and powered by cutting-edge AI! 🚀

---

## ✨ Features

🌟 **Audio Recording**: Detects speech automatically and records user responses.  
📝 **Transcription**: Converts recorded audio into text with **AssemblyAI**.  
🤖 **AI-Generated Responses**: Uses **Google Gemini AI** for natural, conversational replies.  
🎧 **Text-to-Speech**: Brings the bot to life with **ElevenLabs API**, generating human-like audio responses.  
🎟️ **Ticket Interest Assessment**: Summarizes the user's likelihood of purchasing tickets for IGNUS.  

---

## 📋 Requirements

### 🛠️ Libraries

- **AssemblyAI**: For transcribing audio files.
- **Google Generative AI (Gemini)**: For crafting engaging conversational responses.
- **PyPDF2**: To extract detailed information from IGNUS PDF documents.
- **Pygame**: For smooth audio playback of the bot's responses.
- **Pyaudio**: Captures live audio directly from the microphone.  
- **Requests**: Communicates with APIs like **ElevenLabs**.  
- **Numpy**: Efficiently processes audio data.

### 🌐 APIs Needed

🔑 **AssemblyAI API Key**: [Sign Up Here](https://www.assemblyai.com/)  
🔑 **Google Gemini API Key**: [Sign Up Here](https://developers.generativeai.google/)  
🔑 **ElevenLabs API Key**: [Sign Up Here](https://beta.elevenlabs.io/)

### 📂 Environment Variables

Store your API keys securely in an `.env` file:

```env
ASSEMBLY_AI_KEY=your_assembly_ai_key
GEMINAI_API_KEY=your_google_gemini_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```
# 🚀 Installation, Usage, and How It Works

---

## ⚙️ Installation

Follow these steps to set up the **Calling Assistant Bot** on your local machine:

1. **Clone the repository** 📁:

    ```bash
    git clone https://github.com/your-username/IGNUS-Assistant-Bot.git
    ```

2. **Navigate to the project directory** 📂:

    ```bash
    cd IGNUS-Assistant-Bot
    ```

3. **Install dependencies** 📦:

    Ensure you have Python installed on your system. Then, run:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up API keys** 🔑:

    Create a `.env` file in the root directory and add the following variables:

    ```env
    ASSEMBLY_AI_KEY=your_assembly_ai_key
    GEMINAI_API_KEY=your_google_gemini_key
    ELEVENLABS_API_KEY=your_elevenlabs_key
    ```

5. **Verify installation** ✅:

    Run the following command to check if everything is set up correctly:

    ```bash
    python ignus_assistant.py --check
    ```

    This will test API connections and display readiness.

---

## 🎯 Usage

Here’s how to start and use the bot:

1. **Run the bot** 🖥️:

    Start the assistant by running:

    ```bash
    python ignus_assistant.py
    ```

2. **Interactive conversation** 🗣️:

    - The bot will greet the user and initiate the conversation.  
    - Speak clearly when prompted, and the bot will capture your responses.  

3. **Real-time transcription and reply** 🔊:

    - Your voice input will be transcribed and processed.
    - The bot will generate a conversational response and play it back to you.

4. **Ticket assessment summary** 🎟️:

    After the conversation concludes, the bot will evaluate your interest in purchasing tickets and provide a summary.

---

## 🛠️ How It Works

The **Calling Assistant Bot** is powered by advanced AI technologies and works in the following steps:

1. **Conversation Kickoff** 🎤:  
   The bot greets the user and introduces them to the highlights of **IGNUS**, using information extracted from a PDF document.

2. **Audio Input** 🗣️:  
   Users respond verbally, and their speech is recorded using the microphone.

3. **Transcription** ✍️:  
   The bot sends the recorded audio to **AssemblyAI**, which converts it into text for further processing.

4. **AI-Generated Response** 🤖:  
   The transcribed text is processed by **Google Gemini AI**, which generates an intelligent and context-aware response.

5. **Text-to-Speech Conversion** 🔊:  
   The response text is converted into natural-sounding speech using **ElevenLabs API** and played back to the user.

6. **Interest Evaluation** 📈:  
   Based on the user’s responses, the bot determines their interest in purchasing tickets and prepares a final summary.

---

## 🎥 Demo Video

Check out a quick demo of the **Calling Assistant Bot** in action! Click the video below to watch:

[![Voice Bot Demo Video](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](Voice_Bot_Demo_Video.mp4 "Voice Bot Demo Video")


---

### Example Flow

- **Bot**: "Hello! This is a call from IIT Jodhpur regarding our upcoming cultural fest, Ignus. Can we take a moment to talk about it?"
- **User**: "Sure, I’d like to know more."  
- **Bot**: "Ignus is a vibrant cultural extravaganza featuring diverse events and renowned artists. Are you interested in attending?"  
- **User**: "Yes, it sounds exciting!"  

At the end, the bot provides a detailed summary of the conversation and highlights ticket interest. 🎉

---

You're all set to run and interact with the **Calling Assistant Bot**! 🎊

# 🔥 Additional Information

---

## 🌟 Additional Features to Explore

Here are some extra features you could implement to make the **Calling Assistant Bot** even more powerful:

1. **📊 Analytics Dashboard**:  
   - Track call statistics like the number of conversations, user engagement levels, and interest conversion rates.  

2. **🌐 Multi-Language Support**:  
   - Add support for regional and international languages to broaden accessibility.

3. **📱 Mobile Integration**:  
   - Build a mobile app version of the bot to let users manage calls on the go.

4. **💾 Offline Mode**:  
   - Enable offline usage by preloading TTS models and transcripts.

5. **🤝 CRM Integration**:  
   - Connect the bot with Customer Relationship Management (CRM) tools to store user responses and ticket purchase interest data.

---

## 🤝 How to Contribute

We welcome contributions from the community! Here's how you can contribute:

1. **Fork this repository**:  
   Click the `Fork` button at the top of the page.

2. **Clone your fork**:  
   Use the following command to clone your forked repo to your local machine:

    ```bash
    git clone https://github.com/your-username/IGNUS-Assistant-Bot.git
    ```

3. **Create a feature branch**:  
   Work on your changes in a new branch:

    ```bash
    git checkout -b feature/your-feature-name
    ```

4. **Commit your changes**:  
   Save your work with meaningful commit messages:

    ```bash
    git commit -m "Add your feature description"
    ```

5. **Push your changes**:  
   Push the changes to your forked repository:

    ```bash
    git push origin feature/your-feature-name
    ```

6. **Submit a Pull Request (PR)**:  
   Go to the original repository and submit a PR describing your changes.

---

## 🎉 Acknowledgements

We would like to thank the following platforms and tools for making this project possible:

- **AssemblyAI** 📝: For providing high-quality transcription services.  
- **Google Gemini** 🤖: For its exceptional generative AI capabilities.  
- **ElevenLabs** 🎙️: For lifelike text-to-speech services.  
- **Pygame** 🎧: For smooth audio playback.  

---

⭐ If you found this project helpful, don’t forget to give it a star! ⭐


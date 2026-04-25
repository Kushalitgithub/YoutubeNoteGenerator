# YouTube Study Notes Generator

A web app that converts any YouTube lecture or tutorial into structured study notes, flashcards, and Anki decks using AI.

Built with Python, Streamlit, and Groq AI.

---

## Features

- Generate structured study notes from any YouTube video
- Four modes: Brief summary, Detailed notes, Quiz questions, Flashcards
- Subject-aware notes for CS, Math, Physics, Biology, History, Economics
- Output notes in 20 languages including Nepali, Hindi, English and more
- Export as TXT, PDF, or Anki flashcard deck (.apkg)
- Works with both full YouTube links and short youtu.be links

---

## Demo
<img width="688" height="828" alt="image" src="https://github.com/user-attachments/assets/06613c46-bf7b-4be9-9011-c2543e186a06" />
<img width="688" height="828" alt="image" src="https://github.com/user-attachments/assets/52b9543e-fcbb-4630-bbdc-e4924bf8d090" />


---

## Tech Stack

- Python
- Streamlit — web interface
- Groq API — AI note generation (free)
- youtube-transcript-api — fetch video transcripts
- fpdf2 — PDF export
- genanki — Anki deck export

---

## Setup and Installation

### 1. Clone the repository

git clone https://github.com/Kushalitgithub/YoutubeNoteGenerator.git
cd YoutubeNoteGenerator

### 2. Create a virtual environment

python -m venv .venv
source .venv/bin/activate

On Windows:
.venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Set up your API key

Create a .env file in the project folder:

cp .env.example .env

Then open .env and add your free Groq API key.
Get your free key at: https://console.groq.com

### 5. Run the app

streamlit run app.py

Open your browser at http://localhost:8501

## How to Use

1. Paste a YouTube URL into the input box
2. Select your subject from the dropdown
3. Choose your output language
4. Pick a notes mode: Brief, Detailed, Quiz, or Flashcards
5. Click Generate Notes
6. Download as TXT, PDF, or Anki deck

---

## Project Structure

yt-study-notes/
├── app.py              # Streamlit web interface
├── summarizer.py       # Transcript fetching and AI note generation
├── exporter.py         # PDF export
├── flashcard.py        # Flashcard parsing
├── anki_export.py      # Anki deck export
├── .env.example        # API key template (safe to share)
├── .gitignore          # Files excluded from GitHub
└── requirements.txt    # Python dependencies

---

## Getting a Free Groq API Key

1. Go to https://console.groq.com
2. Sign up for a free account
3. Click API Keys and create a new key
4. Copy it into your .env file

---

## Requirements

See requirements.txt:

streamlit
youtube-transcript-api
groq
python-dotenv
fpdf2
genanki
langdetect

---

## Author

Kushal <br>
BCS AI Student at Taylors University <br>
GitHub: https://github.com/Kushalitgithub<br>
LinkedIn: https://www.linkedin.com/in/kushal-bhattarai-960819385/<br>

---

## License

MIT License — free to use and modify

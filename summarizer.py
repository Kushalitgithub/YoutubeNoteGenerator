from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

LANGUAGES = {
    "English": "en",
    "Nepali": "ne",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "Arabic": "ar",
    "Chinese": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "German": "de",
    "Portuguese": "pt",
    "Russian": "ru",
    "Italian": "it",
    "Turkish": "tr",
    "Dutch": "nl",
    "Polish": "pl",
    "Vietnamese": "vi",
    "Thai": "th",
    "Indonesian": "id",
    "Malay": "ms"
}

def get_video_id(url):
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    elif "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    else:
        raise ValueError("Invalid YouTube URL")

def get_transcript(url):
    video_id = get_video_id(url)
    ytt = YouTubeTranscriptApi()

    try:
        # Try to get transcript in any available language
        transcript_list = ytt.list(video_id)
        available = [t.language_code for t in transcript_list]

        # Prefer English, otherwise take first available
        if "en" in available:
            fetched = ytt.fetch(video_id, languages=["en"])
        else:
            fetched = ytt.fetch(video_id, languages=[available[0]])

    except NoTranscriptFound:
        raise Exception("No transcript available for this video.")

    return " ".join([snippet.text for snippet in fetched])

def generate_notes(transcript, mode, output_language, subject):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    subject_hints = {
        "General":          "Extract the main ideas and key points.",
        "Computer Science": "Focus on algorithms, code concepts, data structures, and technical terms.",
        "Mathematics":      "Focus on formulas, theorems, proofs, and step-by-step solutions.",
        "Physics":          "Focus on laws, equations, units, and physical concepts.",
        "Biology":          "Focus on processes, terminology, organisms, and systems.",
        "History":          "Focus on dates, events, key figures, causes, and consequences.",
        "Economics":        "Focus on theories, models, key terms, and real-world examples.",
    }

    mode_instructions = {
        "brief": f"""Summarize this transcript in 5 clear bullet points.
        {subject_hints[subject]}
        Output the response in {output_language}.
        Do not use emojis.""",

        "detailed": f"""Generate structured study notes from this transcript with these sections:
        1. Topic and Overview (2-3 sentences)
        2. Key Concepts (list with short explanations)
        3. Detailed Notes (organized by subtopics)
        4. Quiz Questions (5 questions with answers)
        {subject_hints[subject]}
        Output everything in {output_language}.
        Do not use emojis.""",

        "quiz": f"""Generate 10 quiz questions with answers from this transcript.
        {subject_hints[subject]}
        Number each question clearly.
        Output in {output_language}.
        Do not use emojis.""",

        "flashcards": f"""Generate 10 flashcards from this transcript.
        Format each flashcard EXACTLY like this with no deviation:
        CARD_START
        FRONT: [term or concept]
        BACK: [clear explanation]
        CARD_END
        {subject_hints[subject]}
        Output the FRONT and BACK text in {output_language}.
        Do not use emojis."""
    }

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=2000,
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful study assistant. You create clear structured notes for students. Never use emojis. Always respond in {output_language}."
            },
            {
                "role": "user",
                "content": f"{mode_instructions[mode]}\n\nTranscript:\n{transcript[:8000]}"
            }
        ]
    )

    return response.choices[0].message.content
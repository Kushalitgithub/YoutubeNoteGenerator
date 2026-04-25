import genanki
import random
import re

def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

def create_anki_deck(cards, deck_name="YouTube Study Notes"):
    # Unique IDs for deck and model
    deck_id  = random.randrange(1 << 30, 1 << 31)
    model_id = random.randrange(1 << 30, 1 << 31)

    model = genanki.Model(
        model_id,
        "Simple Model",
        fields=[
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "<h2>{{Question}}</h2>",
                "afmt": "{{FrontSide}}<hr id='answer'><p>{{Answer}}</p>",
            }
        ]
    )

    deck = genanki.Deck(deck_id, clean_text(deck_name))

    for front, back in cards:
        note = genanki.Note(
            model=model,
            fields=[clean_text(front), clean_text(back)]
        )
        deck.add_note(note)

    filename = "study_flashcards.apkg"
    genanki.Package(deck).write_to_file(filename)
    return filename
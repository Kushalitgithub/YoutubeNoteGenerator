def parse_flashcards(notes):
    """Parse the AI output into a list of (front, back) tuples."""
    cards = []

    # Split by CARD_START / CARD_END blocks
    blocks = notes.split("CARD_START")
    for block in blocks:
        if "CARD_END" not in block:
            continue
        block = block.split("CARD_END")[0].strip()

        front, back = "", ""
        for line in block.split("\n"):
            line = line.strip()
            if line.startswith("FRONT:"):
                front = line.replace("FRONT:", "").strip()
            elif line.startswith("BACK:"):
                back = line.replace("BACK:", "").strip()

        if front and back:
            cards.append((front, back))

    return cards

def format_flashcards_text(cards):
    """Format flashcards as readable plain text for TXT/PDF export."""
    lines = []
    for i, (front, back) in enumerate(cards, 1):
        lines.append(f"Card {i}")
        lines.append(f"Q: {front}")
        lines.append(f"A: {back}")
        lines.append("")
    return "\n".join(lines)
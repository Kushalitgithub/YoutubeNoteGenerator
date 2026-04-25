import streamlit as st
from summarizer import get_transcript, generate_notes, LANGUAGES
from exporter import export_pdf
from flashcard import parse_flashcards, format_flashcards_text
from anki_export import create_anki_deck

st.set_page_config(page_title="YT Study Notes", layout="centered")

st.title("YouTube Study Notes Generator")
st.caption("Paste any YouTube lecture and get structured notes, flashcards, or an Anki deck.")

url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns(2)

with col1:
    subject = st.selectbox(
        "Subject",
        ["General", "Computer Science", "Mathematics",
         "Physics", "Biology", "History", "Economics"]
    )

with col2:
    output_language = st.selectbox(
        "Output language",
        list(LANGUAGES.keys())
    )

mode = st.radio(
    "Notes mode",
    options=["brief", "detailed", "quiz", "flashcards"],
    horizontal=True,
    help="Brief = 5 bullets | Detailed = full notes | Quiz = Q&A | Flashcards = study cards"
)

generate = st.button("Generate Notes", use_container_width=True)


if generate:
    if not url:
        st.warning("Please enter a YouTube URL first.")
    else:
        with st.spinner("Fetching transcript..."):
            try:
                transcript = get_transcript(url)
                st.success(f"Transcript fetched — {len(transcript.split())} words")
            except Exception as e:
                st.error(f"Could not get transcript: {e}")
                st.info("Try a video that has captions/subtitles enabled.")
                st.stop()

        with st.spinner("Generating notes..."):
            notes = generate_notes(transcript, mode, output_language, subject)

        st.divider()


        if mode == "flashcards":
            st.subheader("Flashcards")
            cards = parse_flashcards(notes)

            if not cards:
                st.warning("Could not parse flashcards. Showing raw output.")
                st.markdown(notes)
            else:
                st.info(f"{len(cards)} flashcards generated")

                # Show cards as expandable items
                for i, (front, back) in enumerate(cards, 1):
                    with st.expander(f"Card {i}: {front}"):
                        st.write(back)

                st.divider()

                # Download options
                col1, col2, col3 = st.columns(3)

                with col1:
                    txt = format_flashcards_text(cards)
                    st.download_button(
                        "Download TXT",
                        data=txt,
                        file_name="flashcards.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                with col2:
                    pdf_file = export_pdf("Flashcards", format_flashcards_text(cards))
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            "Download PDF",
                            data=f,
                            file_name="flashcards.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

                with col3:
                    anki_file = create_anki_deck(cards)
                    with open(anki_file, "rb") as f:
                        st.download_button(
                            "Download Anki Deck",
                            data=f,
                            file_name="flashcards.apkg",
                            mime="application/octet-stream",
                            use_container_width=True
                        )


        else:
            st.subheader("Your Study Notes")
            st.markdown(notes)

            st.divider()
            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    "Download TXT",
                    data=notes,
                    file_name="study_notes.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        try:
            with col2:
                pdf_file = export_pdf("Study Notes", notes)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        "Download PDF",
                        data=f,
                        file_name="study_notes.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

        except Exception as e:
            st.error(f"Could not generate PDF: {e}")
            st.info("Try downloading the TXT version instead.")
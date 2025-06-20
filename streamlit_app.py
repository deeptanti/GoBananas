import streamlit as st
from youtube_utils import fetch_comments
from azure_utils import detect_language, translate_to_english, analyze_sentiment, extract_key_phrases

st.title("📺 YouTube Comment Analyzer (Multilingual)")

video_url = st.text_input("Enter a YouTube video URL")

if video_url and st.button("Analyze Comments"):
    with st.spinner("Fetching comments..."):
        comments = fetch_comments(video_url)
        if comments:
            st.success(f"Fetched {len(comments)} comments.")
            st.write("### 🔍 Analyzed Comments")

            data = []
            for comment in comments:
                lang = detect_language(comment)
                translated = translate_to_english(comment, lang)
                sentiment = analyze_sentiment(translated)
                key_phrases = extract_key_phrases(translated)
                data.append({
                    "Original": comment,
                    "Lang": lang,
                    "Translated": translated,
                    "Sentiment": sentiment,
                    "Key Phrases": ", ".join(key_phrases)
                })

            # Display in a Streamlit table
            st.dataframe(data)
        else:
            st.error("Failed to fetch comments.")
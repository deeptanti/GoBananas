import streamlit as st
from youtube_utils import fetch_comments
from azure_utils import detect_language, translate_to_english, analyze_sentiment, extract_key_phrases
import pandas as pd

st.set_page_config(page_title="YouTube Comment Analyzer", layout="wide")
st.title("📺 YouTube Comment Analyzer (Multilingual NLP)")
st.markdown("Analyze the top 100 YouTube comments for sentiment, language, and key phrases — with translation support 🌍")

video_url = st.text_input("🎥 Enter a YouTube video link:", placeholder="https://www.youtube.com/watch?v=...")

if video_url and st.button("🚀 Analyze Comments"):
    with st.spinner("Fetching and analyzing comments..."):
        raw_comments = fetch_comments(video_url)
        if not raw_comments:
            st.error("Failed to fetch comments.")
        else:
            enriched = []
            for comment in raw_comments:
                lang = detect_language(comment)
                translation = translate_to_english(comment, lang)
                sentiment = analyze_sentiment(translation)
                phrases = extract_key_phrases(translation)

                enriched.append({
                    "Original": comment,
                    "Language": lang,
                    "Translation": translation,
                    "Sentiment": sentiment.capitalize(),
                    "Key Phrases": ", ".join(phrases)
                })

            df = pd.DataFrame(enriched)

            # Display sentiment summary
            st.subheader("📊 Sentiment Distribution")
            st.bar_chart(df["Sentiment"].value_counts())

            # Display main results table
            st.subheader("📝 Analyzed Comments")

            def sentiment_color(val):
                color_map = {
                    "Positive": "lightgreen",
                    "Negative": "#ff7f7f",
                    "Neutral": "#f0e68c",
                    "Unknown": "#e0e0e0"
                }
                return f"background-color: {color_map.get(val, 'white')}"

            styled_df = df.style.applymap(sentiment_color, subset=["Sentiment"])
            st.dataframe(styled_df, use_container_width=True)

            # Download option
            st.download_button("⬇️ Download Results as CSV", df.to_csv(index=False), file_name="comment_analysis.csv", mime="text/csv")
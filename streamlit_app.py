import streamlit as st
from youtube_utils import fetch_comments

st.title("📺 YouTube Comment Analyzer (Multilingual)")

video_url = st.text_input("Enter a YouTube video URL")

if video_url and st.button("Analyze Comments"):
    with st.spinner("Fetching comments..."):
        comments = fetch_comments(video_url)
        if comments:
            st.success(f"Fetched {len(comments)} comments.")
            for c in comments:
                st.write(f"- {c}")
        else:
            st.error("Failed to fetch comments.")
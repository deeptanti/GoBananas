from googleapiclient.discovery import build
import streamlit as st
import re

def extract_video_id(url):
    pattern = r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def fetch_comments(video_url, max_comments=20):
    api_key = st.secrets["YOUTUBE_API_KEY"]
    video_id = extract_video_id(video_url)
    if not video_id:
        return None

    youtube = build("youtube", "v3", developerKey=api_key)
    comments = []
    next_page_token = None

    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=20,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response["items"]:
            text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(text)
            if len(comments) >= max_comments:
                break
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    return comments
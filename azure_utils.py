import requests
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import streamlit as st

# Azure config from secrets
AZURE_KEY = st.secrets["AZURE_KEY"]
AZURE_ENDPOINT = st.secrets["AZURE_ENDPOINT"]
TRANSLATOR_KEY = st.secrets["AZURE_TRANSLATOR_KEY"]
TRANSLATOR_ENDPOINT = st.secrets["AZURE_TRANSLATOR_ENDPOINT"]

# Initialize Azure Text Analytics client
credential = AzureKeyCredential(AZURE_KEY)
text_analytics_client = TextAnalyticsClient(endpoint=AZURE_ENDPOINT, credential=credential)


def detect_language(comment):
    try:
        response = text_analytics_client.detect_language(documents=[comment])[0]
        return response.primary_language.iso6391_name
    except Exception as e:
        return "und"


def translate_to_english(text, from_lang):
    if from_lang == "en" or from_lang == "(Unknown)":
        return text
    headers = {
        "Ocp-Apim-Subscription-Key": TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": "eastus",
        "Content-type": "application/json"
    }
    params = {"api-version": "3.0", "from": from_lang, "to": "en"}
    body = [{"text": text}]
    try:
        response = requests.post(
            TRANSLATOR_ENDPOINT + "translate",
            params=params,
            headers=headers,
            json=body
        )
        return response.json()[0]["translations"][0]["text"]
    except:
        return text


def analyze_sentiment(text):
    try:
        response = text_analytics_client.analyze_sentiment(documents=[text])[0]
        return response.sentiment
    except:
        return "unknown"


def extract_key_phrases(text):
    try:
        response = text_analytics_client.extract_key_phrases(documents=[text])[0]
        return response.key_phrases
    except:
        return []
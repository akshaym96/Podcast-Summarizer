import streamlit as st
import os
import json
from utils import downloadPodcast, extractHighlights, extractPeople, summary, transcribe
import openai

def load_podcasts(folder_path):
    """
    Iterates through a folder containing jsons and loads as key value, key being enumerated podcast_{i} and value being the json itself
    
    Parameters:
    folder_path (str): The path of the folder containing the json files
    
    Returns:
    dict: A dictionary containing the loaded jsons with keys as enumerated podcast_{i} and values as the json itself
    """
    podcasts = {}
    for i, file_name in enumerate(os.listdir(folder_path)):
        if file_name.endswith(".json"):
            with open(os.path.join(folder_path, file_name), "r") as f:
                podcast = json.load(f)
                podcasts[f"podcast_{i}"] = podcast
    return podcasts

def build_podcast_json(episode_local_url, episode_title, episode_transcription, \
                                     episode_summary, episode_highlights,
                                     episode_guest):

    podcast = {}
    podcast["podcast_title"] = episode_title
    podcast["podcast_thumbnail"] = "assets/today-explained.jpg"
    podcast["podcast_transcript"] = episode_transcription
    podcast["podcast_audio_url"] = episode_local_url
    podcast["podcast_summary"] = episode_summary
    podcast["podcast_key_points"] = episode_highlights
    podcast["podcast_guest"] = episode_guest

    return podcast

# Streamlit app layout
def main(podcasts):

    if "selected_podcast" not in st.session_state:
        # initialize podcasts
        st.session_state.selected_podcast = list(podcasts.keys())[0]  # Initialize with the first podcast

    st.sidebar.header("Existing Feed")
    selected_podcast = st.sidebar.selectbox("Select a podcast", list(podcasts.keys()))

    if st.session_state.selected_podcast != selected_podcast:
        st.session_state.selected_podcast = selected_podcast

    st.sidebar.header("Process new feed")
    access_token = st.sidebar.text_input("Enter OpenAI Access Token", type="password")
    rss_feed = st.sidebar.text_input("Enter RSS Feed Link")

    openai.api_key = access_token

    if st.sidebar.button("Submit"):
        podcast_feed = downloadPodcast.get_podcast_feed(rss_feed)

        episode_local_url, episode_title = downloadPodcast.download_podcast(podcast_feed[0])

        # episode_transcription = transcribe.transcribe_episode(episode_local_url)
        episode_transcription = podcasts[st.session_state.selected_podcast]['podcast_transcript']

        episode_summary = summary.summarize_podcast(episode_transcription, os.path.join("summaries", episode_title + ".txt"))

        episode_highlights = extractHighlights.extract_podcast_highlights(episode_transcription)

        episode_guest = extractPeople.extract_podcast_guest_info(episode_transcription)

        podcast = build_podcast_json(episode_local_url, episode_title, episode_transcription, \
                                     episode_summary, episode_highlights,
                                     episode_guest)

        st.session_state.selected_podcast = podcast

        display_podcast_info(podcast)
        print("Done")

        return

    display_podcast_info(podcasts[st.session_state.selected_podcast])

def display_podcast_info(podcast):
    st.title("Podcast Summarizer")
    st.header(podcast["podcast_title"])

    # Set background image with opacity
    podcast_thumbnail = podcast["podcast_thumbnail"]
    page_bg_img = '''
    <style>
    body {
    background-image: url(f'{podcast_thumbnail}');
    background-size: cover;
    opacity: 0.8;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.image(podcast["podcast_thumbnail"], use_column_width=True)

    audio_url = podcast["podcast_audio_url"]
    st.audio(audio_url, format="audio/mp3")

    st.subheader("Summary")
    st.write(podcast["podcast_summary"])

    st.subheader("Key Points")
    key_points = podcast["podcast_key_points"]
    st.write("\n".join(["- " + point for point in key_points]))

    if 'podcast_guest' in podcast and podcast["podcast_guest"]:        
        st.subheader("Guest Info")
        st.write(podcast["podcast_guest"])


if __name__ == "__main__":
    podcasts = load_podcasts("JsonContent")
    main(podcasts)
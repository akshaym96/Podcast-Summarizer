import streamlit as st
import os
import json

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

# Streamlit app layout
def main(podcasts):
    if "selected_podcast" not in st.session_state:

        # initialize podcasts
        st.session_state.selected_podcast = list(podcasts.keys())[0]  # Initialize with the first podcast

    st.sidebar.header("Options")
    selected_podcast = st.sidebar.selectbox("Select a podcast", list(podcasts.keys()))

    access_token = st.sidebar.text_input("Enter Access Token", type="password")
    
    user_input = st.sidebar.text_area("Enter Your Notes", "Write your notes here...")

    if st.sidebar.button("Submit"):
        if access_token == "your_access_token":  # Replace with your access token
            st.session_state.selected_podcast = selected_podcast

    display_podcast_info(st.session_state.selected_podcast, user_input)

def display_podcast_info(podcast, user_input):
    st.title("Podcast Summarizer")
    st.header(podcasts[podcast]["podcast_title"])

    col1, col2 = st.columns(2)
    col1.image(podcasts[podcast]["podcast_thumbnail"], caption="Thumbnail", use_column_width=True)
    col2.write(f"Duration: {podcasts[podcast]['podcast_audio_duration']}")

    audio_url = podcasts[podcast]["podcast_audio_url"]
    st.audio(audio_url, format="audio/mp3")

    st.subheader("Summary")
    st.write(podcasts[podcast]["podcast_summary"])

    st.subheader("Key Points")
    key_points = podcasts[podcast]["podcast_key_points"]
    st.write("\n".join(["- " + point for point in key_points]))

    st.subheader("Your Notes")
    st.write(user_input)

if __name__ == "__main__":
    podcasts = load_podcasts("JsonContent")
    main(podcasts)
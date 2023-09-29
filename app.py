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

    st.sidebar.header("Existing Feed")
    selected_podcast = st.sidebar.selectbox("Select a podcast", list(podcasts.keys()))

    if st.session_state.selected_podcast != selected_podcast:
        st.session_state.selected_podcast = selected_podcast

    st.sidebar.header("Process new feed")
    access_token = st.sidebar.text_input("Enter OpenAI Access Token", type="password")
    rss_feed = st.sidebar.text_input("Enter RSS Feed Link")

    if st.sidebar.button("Submit"):
        if access_token == "your_access_token":  # Replace with your access token
            st.session_state.selected_podcast = selected_podcast

    display_podcast_info(st.session_state.selected_podcast)

def display_podcast_info(podcast):
    st.title("Podcast Summarizer")
    st.header(podcasts[podcast]["podcast_title"])

    # col1, col2 = st.columns(2)
    # col1.image(podcasts[podcast]["podcast_thumbnail"], caption="Thumbnail", use_column_width=True)
    # col2.write(f"Duration: {podcasts[podcast]['podcast_audio_duration']}")

    # Set background image with opacity
    podcast_thumbnail = podcasts[podcast]["podcast_thumbnail"]
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

    st.image(podcasts[podcast]["podcast_thumbnail"], use_column_width=True)

    audio_url = podcasts[podcast]["podcast_audio_url"]
    st.audio(audio_url, format="audio/mp3")

    st.subheader("Summary")
    st.write(podcasts[podcast]["podcast_summary"])

    st.subheader("Key Points")
    key_points = podcasts[podcast]["podcast_key_points"]
    st.write("\n".join(["- " + point for point in key_points]))

if __name__ == "__main__":
    podcasts = load_podcasts("JsonContent")
    main(podcasts)
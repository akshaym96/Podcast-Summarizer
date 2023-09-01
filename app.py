import streamlit as st

# Sample data for demonstration
podcasts = {
    "Podcast 1": {
        "title": "Title of Podcast 1",
        "thumbnail": "https://example.com/podcast1_thumbnail.jpg",
        "duration": "01:30",
        "audio_url": "https://example.com/podcast1_audio.mp3",
        "summary": "Summary of Podcast 1...",
        "key_points": [
            "Key point 1 from Podcast 1.",
            "Key point 2 from Podcast 1.",
            "Key point 3 from Podcast 1."
        ]
    },
    "Podcast 2": {
        "title": "Title of Podcast 2",
        "thumbnail": "https://example.com/podcast2_thumbnail.jpg",
        "duration": "02:15",
        "audio_url": "https://example.com/podcast2_audio.mp3",
        "summary": "Summary of Podcast 2...",
        "key_points": [
            "Key point 1 from Podcast 2.",
            "Key point 2 from Podcast 2.",
            "Key point 3 from Podcast 2."
        ]
    }
}

# Streamlit app layout
def main():
    if "selected_podcast" not in st.session_state:
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
    st.title("Podcast Details")
    st.header(podcasts[podcast]["title"])

    col1, col2 = st.columns(2)
    col1.image(podcasts[podcast]["thumbnail"], caption="Thumbnail", use_column_width=True)
    col2.write(f"Duration: {podcasts[podcast]['duration']}")

    audio_url = podcasts[podcast]["audio_url"]
    st.audio(audio_url, format="audio/mp3")

    st.subheader("Summary")
    st.write(podcasts[podcast]["summary"])

    st.subheader("Key Points")
    key_points = podcasts[podcast]["key_points"]
    st.write("\n".join(["- " + point for point in key_points]))

    st.subheader("Your Notes")
    st.write(user_input)

if __name__ == "__main__":
    main()
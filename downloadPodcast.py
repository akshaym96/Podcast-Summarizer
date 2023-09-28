import feedparser
import wget
import os
import string

# change the URL as needed
podcast_feed_url = "https://feeds.megaphone.fm/VMP5705694065"
podcast_feed = feedparser.parse(podcast_feed_url)

print("The number of podcast entiries are: ", len(podcast_feed.entries))

def download_podcast(podcast_item):
    """
    Downloads a podcast episode from the given URL and saves it to the current working directory.

    Args:
        podcast_item (dict): A dictionary containing information about the podcast episode, including its URL.

    Returns:
        None
    """

    episode_url = podcast_item.href
    # Extract the episode title from the feed
    episode_title = podcast_feed.entries[0].title

    # Remove any invalid characters from the title
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    episode_title = ''.join(char for char in episode_title if char in valid_chars)

    # Download the episode with the formatted title
    wget.download(episode_url, os.path.join(os.getcwd(), f"{episode_title}.mp3"))

for item in podcast_feed.entries[0].links:
    if(item['type'] == 'audio/mpeg'):
        download_podcast(item)
    
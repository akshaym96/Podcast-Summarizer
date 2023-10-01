import feedparser
import wget
import os
import string
from pathlib import Path

def get_podcast_feed(rss_url):
    print ("Reading full podcast feed")
    print ("Feed URL: ", rss_url)

    # Read from the RSS Feed URL
    import feedparser
    intelligence_feed = feedparser.parse(rss_url)
    podcast_title = intelligence_feed['feed']['title']
    podcast_link = intelligence_feed['feed']['link']
    podcast_image = intelligence_feed['feed']['image'].href
    podcast_feed = []
    for item in intelligence_feed.entries:
        episode_title = item['title']
        episode_date = item['published']
        try:
            season = item ['itunes_season']
        except:
            season = ''

        try:
            episode = item ['itunes_episode']
        except:
            episode = ''
        for item in item.links:
            if (item['type'] == 'audio/mpeg'):
                episode_audio_url = item.href
        podcast_feed.append({
        "podcast_title": podcast_title,
        "podcast_link": podcast_link,
        "podcast_image": podcast_image,
        "episode_title": episode_title,
        "episode_date": episode_date,
        "episode_season": season,
        "episode_episode": episode,
        "episode_audio_url": episode_audio_url
        })
    print ("RSS URL Read: ", podcast_feed)
    
    return podcast_feed


def download_podcast_audio(episode_name, episode_url, assets_path):    
    # Download the podcast episode by parsing the RSS feed

    p = Path(assets_path)
    p.mkdir(exist_ok=True)

    episode_path = p.joinpath(episode_name)
    print ("Downloading the podcast episode")
    import requests
    with requests.get(episode_url, stream=True) as r:
        r.raise_for_status()
        with open(episode_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print ("Podcast Episode downloaded")
    print(episode_path)
    return episode_path

# download_podcast(podcast_feed[0])
def download_podcast(podcast_feed_item, assets_path="assets"):
    """
    Downloads a podcast episode from the given URL and saves it to the current working directory.

    Args:
        podcast_item (dict): A dictionary containing information about the podcast episode, including its URL.

    Returns:
        None
    """

    # Extract the episode title from the feed
    episode_title = podcast_feed_item['episode_title']
    # Remove any invalid characters from the title
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    episode_title = ''.join(char for char in episode_title if char in valid_chars)
    episode_name = episode_title
    episode_title = '_'.join(episode_name.split())


    episode_filename = f"{episode_title}.mp3"
    
    print ("Item: ", episode_title)
    
    episode_url = podcast_feed_item['episode_audio_url']

    download_podcast_audio(episode_filename, episode_url, assets_path)
    return os.path.join(assets_path, episode_filename), episode_name 

# for item in podcast_feed.entries[0].links:
#     if(item['type'] == 'audio/mpeg'):
#         download_podcast(item)
    
# Sticking the podcast length to around 30-40 mins for latency and cost incurred through API calls
# Also longer the podcast, the longer it takes to transcribe, depending on the GPU used as well.

# Alternative is to chunk the podcast and transribe in bits and pieces, might be useful for longer podcasts

import pathlib
import whisper
import os
import openai

# NOTE: Perform download only once and save to storage    
def download_whisper():
    
    model_path = pathlib.Path("../medium.pt")
    if model_path.exists():
        print("Model has been downloaded, no re-download necessary")
    else:
        print ("Starting download of Whisper Model")
        whisper._download(whisper._MODELS["medium"], 
                        os.getcwd(),
                        False)


# Load model from saved location. Better to have a GPU, atleast a single GPU machine to run
model = whisper.load_model('medium', device='cpu', download_root='../')

def transcribe_episode(episode_local_url):

    # change the name of the podcast accordingly
    # Can take time for the transcription

    # TODO: Use smaller audio files, this can error out easily
    print ("Starting Podcast Transcription Function")
    audio_file= open(episode_local_url, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    return transcript

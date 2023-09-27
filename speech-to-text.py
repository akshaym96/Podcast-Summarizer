# Sticking the podcast length to around 30-40 mins for latency and cost incurred through API calls
# Also longer the podcast, the longer it takes to transcribe, depending on the GPU used as well.

# Alternative is to chunk the podcast and transribe in bits and pieces, might be useful for longer podcasts

import pathlib
import whisper
import os

# NOTE: Perform download only once and save to storage    
def download_whisper():
    
    model_path = pathlib.Path("/content/podcast/medium.pt")
    if model_path.exists():
        print("Model has been downloaded, no re-download necessary")
    else:
        print ("Starting download of Whisper Model")
        whisper._download(whisper._MODELS["medium"], 
                        os.getcwd(),
                        False)


# Load model from saved location. Better to have a GPU, atleast a single GPU machine to run
model = whisper.load_model('medium', device='cuda', download_root=os.getcwd())

# change the name of the podcast accordingly
# Can take time for the transcription
result = model.transcribe("/content/podcast_episode.mp3")

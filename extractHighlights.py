import openai
import json
import wikipedia

def extract_podcast_highlights(podcast_file_path):
    """
    Extracts highlights from a podcast transcript using OpenAI's GPT-3 model.

    Args:
    podcast_file_path (str): The file path of the podcast transcript.

    Returns:
    str: A string containing the highlights from the podcast transcript.
    """

    try:
        podcast_transcript = ""
        with open(podcast_file_path, 'r') as file:
            podcast_transcript = file.read()

        # Use OpenAI's GPT-3 model to extract highlights from the podcast transcript
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": podcast_transcript}],
            functions=[
            {
                "name": "get_podcast_highlights",
                "description": "Extract some of the highlights from the podcast text and list them down using bulleted points. Use only upto 5 list items.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "highlights": {
                            "type": "string",
                            "description": "The list of highlights from the podcast",
                        }
                    },
                    "required": ["highlights"],
                },
            }
        ],
        function_call={"name": "get_podcast_highlights"}
        )

        podcast_highlights = ""
        response_message = completion["choices"][0]["message"]
        if response_message.get("function_call"):
            function_name = response_message["function_call"]["name"]
            function_args = json.loads(response_message["function_call"]["arguments"])
            podcast_highlights=function_args.get("highlights")

        # Print and return the highlights from the podcast transcript
        print ("Highlights from the podcast: ", podcast_highlights)
        return podcast_highlights

    except Exception as e:
        print("Error occurred: ", e)
        return "Highlights unavailable"

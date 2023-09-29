import openai
import json
import wikipedia

def extract_podcast_guest_info(podcast_transcript):
    """
    Extracts information about the podcast guest using their full name and the name of the organization they are part of to search for them on Wikipedia or Google.

    Args:
    episode_transcript (str): transcript of the podcast.

    Returns:
    str: The summary of the podcast guest's information retrieved from Wikipedia.

    Raises:
    Exception: If an error occurs while retrieving the information from Wikipedia.
    """
    try:
        print("Extracting guest info....")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[{"role": "user", "content": podcast_transcript}],
            functions=[
            {
                "name": "get_podcast_guest_information",
                "description": "Get information on the podcast guest using their full name and the name of the organization they are part of to search for them on Wikipedia or Google",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "guest_name": {
                            "type": "string",
                            "description": "The full name of the guest who is speaking in the podcast",
                        },
                        "guest_organization": {
                            "type": "string",
                            "description": "The full name of the organization that the podcast guest belongs to or runs",
                        },
                        "guest_title": {
                            "type": "string",
                            "description": "The title, designation or role of the podcast guest in their organization",
                        },
                    },
                    "required": ["guest_name"],
                },
            }
        ],
        function_call={"name": "get_podcast_guest_information"}
        )

        podcast_guest = ""
        podcast_guest_org = ""
        podcast_guest_title = ""
        response_message = completion["choices"][0]["message"]
        if response_message.get("function_call"):
            function_name = response_message["function_call"]["name"]
            function_args = json.loads(response_message["function_call"]["arguments"])
            podcast_guest=function_args.get("guest_name")
            podcast_guest_org=function_args.get("guest_organization")
            podcast_guest_title=function_args.get("guest_title")

        if podcast_guest_org is None:
            podcast_guest_org = ""
        if podcast_guest_title is None:
            podcast_guest_title = ""

        first_person  = podcast_guest.split(",")[0]

        print ("Podcast Guest is ", first_person)

        guest_info = wikipedia.page(first_person + " " + podcast_guest_org + " " + podcast_guest_title, auto_suggest=False)

        podcast_guest_info = guest_info.summary

        return podcast_guest_info

    except Exception as e:
        print("Error occurred: ", e)
        return "Guest Information unavailable"

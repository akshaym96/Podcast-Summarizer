import openai
import json
import wikipedia

def extract_podcast_guest_info(summary_file_path):
    try:
        podcast_summary = ""
        with open(summary_file_path, 'r') as file:
            podcast_summary = file.read()

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": podcast_summary}],
            functions=[
            {
                "name": "get_podcast_mainPerson_information",
                "description": "extract the name of main character mentioned in the user input separated by a comma",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "guest_name": {
                            "type": "string",
                            "description": "List of the guest names extracted from user input",
                        },
                        "unit": {"type": "string"},
                    },
                    "required": ["guest_name"],
                },
            }
            ],
            function_call={"name": "get_podcast_mainPerson_information"}
            )

        podcast_guest = ""
        response_message = completion["choices"][0]["message"]
        if response_message.get("function_call"):
            function_name = response_message["function_call"]["name"]
            function_args = json.loads(response_message["function_call"]["arguments"])
            podcast_guest=function_args.get("guest_name")

        first_person  = podcast_guest.split(",")[0]

        print ("Podcast Guest is ", first_person)

        guest_info = wikipedia.page(first_person, auto_suggest=False)

        podcast_guest_info = guest_info.summary

        return podcast_guest_info

    except Exception as e:
        print("Error occurred: ", e)
        return "Guest Information unavailable"

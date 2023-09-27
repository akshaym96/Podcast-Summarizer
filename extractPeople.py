import openai

podcast_summary = ""
with open('summaries/summary1.txt', 'r') as file:
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


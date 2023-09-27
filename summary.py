import openai
import tiktoken

def summarize_podcast(podcast_transcript_file, output_file):
    # Load the podcast transcript
    with open(podcast_transcript_file, "r") as file:
        podcast_transcript = file.read()

    # Encode the transcript using the GPT-3.5-Turbo model
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    encoded_transcript = enc.encode(podcast_transcript)

    # Construct the instruction prompt and request
    instruct_prompt = """
    Summarize the text presented to you. This text is taken from a podcast. Remember to include important points and details in the summary.
    Include details of all the persons mentioned in the summary.
    """
    request = instruct_prompt + podcast_transcript

    # Use the GPT-3.5-Turbo-16k model to generate a summary
    chatOutput = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k",
                                            messages=[{"role": "system", "content": "You are a helpful assistant."},
                                                      {"role": "user", "content": request}
                                                      ]
                                            )

    podcastSummary = chatOutput.choices[0].message.content

    # Write the podcast summary to a file
    with open(output_file, "w") as file:
        file.write(podcastSummary)

    return podcastSummary

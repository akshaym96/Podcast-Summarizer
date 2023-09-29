import openai
import tiktoken

def summarize_podcast(podcast_transcript, output_file):
    """
    This function takes a podcast transcript  and generates a summary of the podcast using the GPT-3.5-Turbo-16k model.
    The summary is then written to an output file and returned as a string.

    Args:
        podcast_transcript_file (str): The file path of the podcast transcript.
        output_file (str): The file path of the output file where the summary will be written.

    Returns:
        str: The summary of the podcast as a string.
    """
    print("Summarizing......")
    # Encode the transcript using the GPT-3.5-Turbo model
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo-16k")
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

    print("Summarizing done")

    return podcastSummary

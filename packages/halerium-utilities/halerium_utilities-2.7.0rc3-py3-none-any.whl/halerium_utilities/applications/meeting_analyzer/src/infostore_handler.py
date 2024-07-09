# infrastructure imports
import json
from datetime import datetime

# halerium_utilities imports
from halerium_utilities.prompt.models import call_model

# backend imports
from .infostore_utils import add_chunks_to_vectorstore, get_information_store_info, get_workspace_information_stores


SYSTEM_MESSAGE_TRANSCRIPTS = """
You are a expert that in chunking text and assigning Metda Data to it. You are super reliable in theformat you give out your solution. You always reply with a json of chunks. no further text or explanations.

Your task is to split a meeting transcript into structured sections. For each section, adhere to the following consistent format:

- **Title**: Provide a clear and concise title that encapsulates the main point or topic of the section.

- **Transcript Chunk**: Directly quote the portion of the transcript that pertains to the section you are summarizing.

- **Participants**: [List the names of participants involved in this section if provided]
- **Meeting Topic**: [State the overarching topic or title of the meeting]
- **Section Topic**: [Indicate the specific agenda item or topic covered in this section]

Ensure that each section is self-contained, providing sufficient context to be understood on its own. The sections should be formatted to enable easy searchability by keywords or questions related to their content. Consistency in format is key to facilitate straightforward retrieval by an LLM when queried. Create distinct sections for different topics discussed to maintain clarity and organization. DO not number the chunks you give out.
Important Note: every part of the transcript should be assigned to a specific chunk. you don't skip or ignore parts of the transcripts
"""
SYSTEM_MESSAGE_SUMMARIES = """
You are a helpful assistant who derives a title for a given text about some insights/summary about a meeting transcript. The text you get can be a summary of the whole meeting or a subsummary/insights of a specific perspective/part of the meeting. Your answers must have the following format: \"title: ...\". no further explanation or rephrasing.
"""


def fetch_infostore(name:str):
    """
    Fetches the information store with the given name.

    Args:
        name (str): Name of the information store to fetch.

    Returns:
        str: Information store id.
    """
    # retrieve the information stores of the current workspace
    stores = get_workspace_information_stores()['items']

    # get the corresponding info store id
    info_store_id = None
    for store in stores:
        if store.get('name') == name:
            info_store_id = store.get('uuid')
            break

    # get the vectorstore id
    store_info = get_information_store_info(info_store_id)
    vectorstore_id = store_info["item"]["vectorstores"][0]["id"]
    return vectorstore_id


def push_summaries_to_infostore(list_of_text: list, info_store_name: str = "SummariesStore"):
    """
    Pushes the given list of text to the information store with the given name.

    Args:
        list_of_text (list): List of text to push to the information store.
        info_store_name (str, optional): Name of the information store to push the text to. Defaults to "testStore".
    """
    # get the vectorstore id
    vectorstore_id = fetch_infostore(info_store_name)

    # prepare the chunks
    chunks = []
    today = datetime.now().strftime("%Y-%m-%d")

    for chunk in list_of_text:
        body_detailed = {
            "messages": [
                {"role": "system", "content": SYSTEM_MESSAGE_SUMMARIES},
                {"role": "user", "content": f"Given these insights of a meeting transcript: {chunk}.\n give it a good title. The title should not be long, just 1-2 sentences maximum."}
            ]
        }
        
        # build up the metadata
        gen = call_model("chat-gpt-35", body=body_detailed, parse_data=True)
        
        gp_metadata = ""
        for sse in gen:
            gp_metadata += sse.data.get("chunk","")

        # build the entry
        entry = {
            "content": gp_metadata + "\n" + today + "\n" + chunk,
            "metadata": {"date": f"{today}"}
        }
        chunks.append(entry)

    # push the information to the vectorstore
    add_chunks_to_vectorstore(vectorstore_id, chunks)


def push_transcript_to_infostore(transcript: str, info_store_name: str = "TranscriptsStore"):
    """
    Pushes the given transcript to the information store with the given name.

    Args:
        transcript (str): Transcript to push to the information store.
        info_store_name (str, optional): Name of the information store to push the transcript to. Defaults to "transStore".
    """
    chunks = []
    today = datetime.now().strftime("%Y-%m-%d")
    # get the vectorstore id
    vectorstore_id = fetch_infostore(info_store_name)

    # prepare body request for the model
    body = {
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE_TRANSCRIPTS},
            {"role": "user", "content": f"Given this meeting transcript: {transcript}.\n Chunk it."}
        ]
    }

    # call the model to get the chunks
    gen = call_model("chat-gpt-40-o", body=body, parse_data=True)
    response = ""
    for sse in gen:
        response += sse.data.get("chunk","")

    response = json.loads(response.replace("\n","").replace("```json","").replace("```",""))

    for chunk in response:
        content = ""
        for key, value in chunk.items():
            content += f"{key}: {str(value)}\n"
        entry = {
            "content": content,
            "metadata": {
                "date": f"{today}"},
        }

        chunks.append(entry)

    # push the information to the vectorstore
    add_chunks_to_vectorstore(vectorstore_id, chunks)

if __name__ == "__main__":
    push_summaries_to_infostore(["This is a dummy text for the year 1998", "this is another dummy text for the year 2002"])
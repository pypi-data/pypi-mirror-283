from halerium_utilities.prompt.models import call_model
import json


def transcribe_audio(audio_b64: str) -> dict:

    body = {"audio": audio_b64}
    r = call_model("nova2", body=body)

    ans = ""
    for sse in r:
        if json.loads(sse.data).get("chunk"):
            ans += json.loads(sse.data).get("chunk")

    return ans

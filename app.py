from flask import Flask, render_template, request
from elevenlabs import generate
from pydub import AudioSegment
from openai import OpenAI
import eng_to_ipa as ipa
import base64
import uuid
import io

message_storage = {}

app = Flask(__name__)
client = OpenAI()

def audio_duration(audio_bytes):
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
    return len(audio)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/message", methods=["POST"])
def message():
    global message_storage

    message_history = []
    session = request.json.get("session") or str(uuid.uuid4())

    if session not in message_storage:
        message_storage[session] = []

    message_history = message_storage[session]

    user_message = {
        "role": "user",
        "content": request.json["message"]
    }
    message_history.append(user_message)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are Santa Claus. Answer as Santa Claus talking to a child, in 1-5 sentences. Be funny.",
            }
        ] + message_history
    )

    message = response.choices[0].message
    message_text = message.content

    message_history.append(message)

    if len(message_history) > 4:
        message_history.pop(0)

    if len(message_storage.keys()) > 50:
        message_storage = {}

    if os.getenv("SPEECH_API") == "elevenlabs":
        audio = generate(message_text, voice="Oswald")
    else:
        audio = client.audio.speech.create(
            input=message_text,
            model="tts-1",
            voice="onyx",
        ).read()

    audio_b64 = base64.b64encode(audio).decode("utf-8")

    return {
        "audio": audio_b64,
        "response": message_text,
        "ipa": ipa.convert(message_text),
        "duration": audio_duration(audio),
        "session": session,
    }

if __name__ == "__main__":
    app.run(debug=True)

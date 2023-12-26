from flask import Flask, render_template, request
from elevenlabs import generate
from pydub import AudioSegment
from openai import OpenAI
import eng_to_ipa as ipa
import base64
import io

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
    print("Message: " + request.json["message"])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are Santa Claus. Answer as Santa Claus talking to a child. Be funny.",
            },
            {
                "role": "user",
                "content": request.json["message"]
            }
        ]
    )

    message = response.choices[0].message
    message_text = message.content

    print("Response: " + message_text)

    audio = generate(message_text, voice="Oswald")
    audio_b64 = base64.b64encode(audio).decode("utf-8")

    return {
        "audio": audio_b64,
        "response": message_text,
        "ipa": ipa.convert(message_text),
        "duration": audio_duration(audio),
    }

if __name__ == "__main__":
    app.run(debug=True)

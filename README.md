# Santa-GPT

Talk to Santa Claus with your voice, and he answers with his voice. Try it out: https://santa.talking-gpt.com

## Quick Start

```console
$ pip install -r requirements.txt
$ python3 app.py
$ google-chrome http://localhost:5000
```

## API-keys

You need to have your OpenAI API key in the `OPENAI_API_KEY` environment variable:

```console
$ export OPENAI_API_KEY=YOUR_API_KEY
```

## Text-to-Speech API

By default, it uses OpenAI text-to-speech API for the voice generation.

If you want to use ElevenLabs for text-to-speech, you also need to add your ElevenLabs API key to your environment and set the `SPEECH_API` environment variable to `elevenlabs`:

```console
$ export ELEVEN_API_KEY=YOUR_API_KEY
SPEECH_API=elevenlabs
```

## Changing the voice

You can change the voice with the `VOICE_NAME` environment variable:

```console
$ export VOICE_NAME=Oswald
```

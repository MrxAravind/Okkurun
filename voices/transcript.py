# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.

import assemblyai as aai

# Replace with your API key
aai.settings.api_key = "fbbd2132e5fb4731a9b07d9c92c1bc8e"

# URL of the file to transcribe
FILE_URL = "https://assemblyaiusercontent.com/playground/XB-Sv8PuuuU.mp3"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

# You can set additional parameters for the transcription
config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best, language_detection=True)

transcriber = aai.Transcriber(config=config)
transcript = transcriber.transcribe(FILE_URL)

if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
else:
    print(transcript.export_subtitles_srt())
import assemblyai as aai
from config import ASSEMBLY_AI_API_KEY


aai.settings.api_key = ASSEMBLY_AI_API_KEY

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
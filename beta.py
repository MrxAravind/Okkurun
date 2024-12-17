import os
import uuid
import requests
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
from termcolor import colored
from dotenv import load_dotenv
from datetime import timedelta
import assemblyai as aai

# Load API key from .env
load_dotenv("../.env")
ASSEMBLY_AI_API_KEY = os.getenv("ASSEMBLY_AI_API_KEY")


def save_video(video_url: str, directory: str = "../temp") -> str:
    """Download and save a video from a URL."""
    video_path = f"{directory}/{uuid.uuid4()}.mp4"
    with open(video_path, "wb") as f:
        f.write(requests.get(video_url).content)
    return video_path


def generate_subtitles_assemblyai(audio_path: str, voice: str) -> str:
    """Generate subtitles using AssemblyAI."""
    aai.settings.api_key = ASSEMBLY_AI_API_KEY
    language_code = {"br": "pt", "id": "en", "jp": "ja", "kr": "ko"}.get(voice, voice)
    transcriber = aai.Transcriber(config=aai.TranscriptionConfig(language_code=language_code))
    transcript = transcriber.transcribe(audio_path)
    return transcript.export_subtitles_srt()


def generate_subtitles_locally(sentences, audio_clips) -> str:
    """Generate subtitles locally based on sentences and audio clips."""
    def convert_to_srt_time(seconds):
        return str(timedelta(seconds=seconds)).split(".")[0].replace(",", ",") + ",000"

    subtitles = []
    start_time = 0
    for i, (sentence, clip) in enumerate(zip(sentences, audio_clips), start=1):
        end_time = start_time + clip.duration
        subtitles.append(f"{i}\n{convert_to_srt_time(start_time)} --> {convert_to_srt_time(end_time)}\n{sentence}\n")
        start_time = end_time
    return "\n".join(subtitles)


def generate_subtitles(audio_path: str, sentences, audio_clips, voice: str) -> str:
    """Generate subtitles, either via AssemblyAI or locally."""
    subtitles_path = f"../subtitles/{uuid.uuid4()}.srt"
    if ASSEMBLY_AI_API_KEY:
        print(colored("[+] Creating subtitles using AssemblyAI", "blue"))
        subtitles = generate_subtitles_assemblyai(audio_path, voice)
    else:
        print(colored("[+] Creating subtitles locally", "blue"))
        subtitles = generate_subtitles_locally(sentences, audio_clips)
    
    with open(subtitles_path, "w") as file:
        file.write(subtitles)
    
    print(colored("[+] Subtitles generated.", "green"))
    return subtitles_path


def combine_videos(video_paths, max_duration, max_clip_duration, threads) -> str:
    """Combine videos into a single video."""
    combined_video_path = f"../temp/{uuid.uuid4()}.mp4"
    clips = []
    tot_dur = 0
    for video_path in video_paths:
        clip = VideoFileClip(video_path).without_audio().subclip(0, min(max_clip_duration, max_duration - tot_dur)).resize((1080, 1920))
        clips.append(clip)
        tot_dur += clip.duration
        if tot_dur >= max_duration:
            break

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(combined_video_path, threads=threads)
    return combined_video_path


def generate_video(combined_video_path: str, tts_path: str, subtitles_path: str, threads: int, subtitles_position: str, text_color: str) -> str:
    """Generate final video with audio and subtitles."""
    generator = lambda txt: TextClip(txt, font="../fonts/bold_font.ttf", fontsize=100, color=text_color, stroke_color="black", stroke_width=5)
    horizontal, vertical = subtitles_position.split(",")
    subtitles = SubtitlesClip(subtitles_path, generator)

    result = CompositeVideoClip([VideoFileClip(combined_video_path), subtitles.set_pos((horizontal, vertical))])
    audio = AudioFileClip(tts_path)
    result = result.set_audio(audio)

    output_path = "../temp/output.mp4"
    result.write_videofile(output_path, threads=threads)
    return output_path

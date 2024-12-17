import requests

def download_audio_samples(voice, text):
    response = requests.post(
            'https://streamlabs.com/polly/speak',
            headers={'Referer': 'https://streamlabs.com/'},
            data={'voice': voice, 'text': text, 'service': 'polly'}
        )
        
    speak_url = response.json().get('speak_url')
        
    if speak_url:
            # Download the audio file
            with open(f"sample_{voice}.mp3", 'wb') as f:
                f.write(requests.get(speak_url).content)
            print(f"Downloaded sample_{voice}.mp3")
    else:
            print(f"Error: Could not get speak_url for {voice}")

# Example usage
voices = ["Brian", "Emma", "Russell", "Joey", "Matthew"]
text = """The person is young and feels that death is still far away, but they are terrified of it. They are scared of their body turning to dust or being eaten by worms. This fear has been growing each day, and sometimes it causes physical pain, like difficulty breathing and chest pain. They admit it might sound extreme, but this fear has only started recently. They're wondering if others feel the same way and how they cope with it."""
for i in voices:
    download_audio_samples(i, text)

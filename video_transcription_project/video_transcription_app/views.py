import requests
import speech_recognition as sr
from django.shortcuts import render
from pydub import AudioSegment
from .models import Video

def transcribe_video(request):
    if request.method == 'POST':
        # Get the video URL from the POST request
        video_url = request.POST['video_url']

        # Download the video using requests library
        response = requests.get(video_url)
        with open('video.mp4', 'wb') as f:
            f.write(response.content)

        # Convert the video to audio using pydub library
        audio = AudioSegment.from_file('video.mp4', 'mp4')
        audio.export('audio.wav', format='wav')

        # Transcribe the audio using SpeechRecognition library
        r = sr.Recognizer()
        with sr.AudioFile('audio.wav') as source:
            audio = r.record(source)
            transcript = r.recognize_google(audio)

        # Save the video URL and transcript to the database
        Video.objects.create(video_url=video_url, transcript=transcript)

        # Render the transcription result template with the transcript
        return render(request, 'transcription_result.html', {'transcript': transcript})

    # Render the video upload template for GET requests
    return render(request, 'transcribe_video.html')

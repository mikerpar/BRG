import os
import shutil
import random
from gtts import gTTS
from dotenv import load_dotenv
from google.cloud import texttospeech
from google.oauth2 import service_account

output_path = "./video_output"
audio_workspace = "./audio_workspace"
background_clip_path = "./background_clips"

language = 'en'

def GetFileCount(path):
    return len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])

def SelectRandomBackgroundClip():
    total_bg_clips = GetFileCount(background_clip_path)
    selected_num = random.choice(range(0, total_bg_clips))
    list_of_bg_clips = [f for f in os.listdir(background_clip_path) if os.path.isfile(os.path.join(background_clip_path, f))]
    return list_of_bg_clips[selected_num]

def GenerateVideoName():
    return "video" + str(GetFileCount(output_path) + 1) + ".mp4"

def GenerateAudioName():
    return "audio" + str(GetFileCount(audio_workspace) + 1) + ".mp3"

def GetTTSAPIKey():
    load_dotenv()
    api_key =  os.getenv('GOOGLE_TTS_API_KEY')
    if api_key:
        return api_key
    else:
        exit(-1)

def GetApplicationCredentialsJSON():
    load_dotenv()
    credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if credentials_json:
        return credentials_json
    else:
        exit(-1)

def GetDisplayWordsWithDurations(text):
    os.environ["GOOGLE_API_KEY"] = GetTTSAPIKey()
    cred = GetApplicationCredentialsJSON()
    credentials = service_account.Credentials.from_service_account_file(
        cred
    )
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        name="en-US-Wavenet-D"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )


    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)

    return 0

def GenerateAudioFromText(text, filename):
    os.environ["GOOGLE_API_KEY"] = GetTTSAPIKey()
    cred = GetApplicationCredentialsJSON()
    credentials = service_account.Credentials.from_service_account_file(
        cred
    )
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        name="en-US-Wavenet-D"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(audio_workspace + "\\" + filename, "wb") as out:
        out.write(response.audio_content)

def CleanAudioWorkspace():
    if os.path.exists(audio_workspace):
        shutil.rmtree(audio_workspace)
    os.makedirs(audio_workspace)

def GenerateWordAudioMap(textblock):
    CleanAudioWorkspace()
    wordlist = textblock.split()
    filenames = []
    for word in wordlist:
        filename = GenerateAudioName()
        filenames.append(filename)
        GenerateAudioFromText(word, filename)
    return dict(zip(wordlist, filenames))

def GenerateAudioClip(text):
    filename = GenerateAudioName()
    GenerateAudioFromText(text, filename)
    return ".\\audio_workspace\\" + filename

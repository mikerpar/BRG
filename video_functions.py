from moviepy import *
from util import *
from moviepy.video.fx.Crop import Crop
from moviepy.video.fx.Resize import Resize

output_path = "./video_output/"
resolution = (1080, 1920)

def ResizeBackgroundClip(clip):
    original_width, original_height = clip.size
    target_width, target_height = resolution
    crop_x1 = (original_width - target_width) // 2
    crop_y1 = (original_height - target_height) // 2
    crop_x2 = crop_x1 + target_width
    crop_y2 = crop_y1 + target_height
    
    cropped_clip = Crop(x1=crop_x1, y1=crop_y1, x2=crop_x2, y2=crop_y2).apply(clip)
    resized_clip = Resize(new_size=(target_width, target_height)).apply(cropped_clip)
    return resized_clip

def TrimBackgroundClip(clip, duration):
    start_limit = clip.duration - duration
    start = random.uniform(0, start_limit)
    return clip.subclipped(start_time=start, end_time=start + duration)

def GenerateTextClipsWithAudio(text, word_audio_map):
    text_clips = []
    audio_clips = []
    for key, value in word_audio_map.items():
        audio = AudioFileClip(".\\audio_workspace\\" + value)
        duration = audio.duration - 0.45
        text_clip = TextClip(size=resolution, text=key, duration=duration, font="arial", font_size=70, color='white')
        audio_clips.append(audio)
        text_clips.append(text_clip)
    return text_clips, audio_clips

def GetBackgroundClip(duration):
    filename = SelectRandomBackgroundClip()
    video_clip = VideoFileClip(".\\background_clips\\" + filename)
    video_clip = ResizeBackgroundClip(video_clip)
    return TrimBackgroundClip(video_clip, duration)

def SumDuration(word_audio_map):
    duration = 0
    for key, value in word_audio_map.items():
        audio = AudioFileClip(".\\audio_workspace\\" + value)
        duration += audio.duration
        audio.close()
    return duration

def CombineTextClips(text_clips):
    return concatenate_videoclips(text_clips)

def CombineAudioClips(audio_clips):
    return concatenate_audioclips(audio_clips)

def CombineTextAndBackgroundClips(text):
    word_audio_map = GenerateWordAudioMap(text)
    audio_clip = AudioFileClip(GenerateAudioClip(text))
    duration_sum = SumDuration(word_audio_map)
    text_clips, audio_clips = GenerateTextClipsWithAudio(text, word_audio_map)
    text_clip = CombineTextClips(text_clips)
    video_clip = CompositeVideoClip([GetBackgroundClip(duration_sum), text_clip])
    video_clip = video_clip.with_audio(audio_clip)
    return video_clip

def OutputVideo(clip):
    clip.write_videofile(output_path + GenerateVideoName(), fps=24)
#word_audio_map = GenerateWordAudioMap(text)
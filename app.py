# كود من كتابة: أبو سعد عبدالرحمن المصلوخي
import os
from gtts import gTTS
from moviepy.editor import *

# وظيفة لإنشاء الصوت من النص
def create_audio(text, output_file="audio.mp3"):
    tts = gTTS(text, lang="ar")
    tts.save(output_file)
    return output_file

# وظيفة لإنشاء الفيديو
def create_video(quran_text, background_video, output_file="final_video.mp4"):
    # إنشاء ملف الصوت
    audio_file = create_audio(quran_text)

    # تحميل فيديو الخلفية
    video = VideoFileClip(background_video)

    # إنشاء النص وإضافته للفيديو
    txt_clip = TextClip(quran_text, fontsize=70, color='white', font="Arial", bg_color="black")
    txt_clip = txt_clip.set_position('center').set_duration(video.duration)

    # تحميل الصوت
    audio = AudioFileClip(audio_file)

    # دمج الفيديو والنص والصوت
    final_video = CompositeVideoClip([video, txt_clip]).set_audio(audio)

    # تصدير الفيديو النهائي
    final_video.write_videofile(output_file, fps=24, codec="libx264")
    return output_file

# النص القرآني
quran_text = "إِنَّ مَعَ الْعُسْرِ يُسْرًا"
background_video = "background.mp4"  # يجب رفع ملف الخلفية مع الكود

# إنشاء الفيديو النهائي
create_video(quran_text, background_video)
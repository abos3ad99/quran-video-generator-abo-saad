
import streamlit as st
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import requests
import numpy as np

st.title("تطبيق لتوليد فيديوهات بالآيات القرآنية")

# إدخال النصوص وروابط الملفات
quranic_text = st.text_input("أدخل الآية القرآنية:", "إِنَّ اللَّهَ مَعَ الصَّابِرِينَ")
video_url = st.text_input("رابط فيديو الخلفية:", "https://samplelib.com/lib/preview/mp4/sample-5s.mp4")
audio_url = st.text_input("رابط صوت التلاوة:", "https://download.quranicaudio.com/quran/mishaari_raashid_al_3afaasee/001.mp3")

if st.button("توليد الفيديو"):
    try:
        # تحميل الفيديو والصوت
        video_response = requests.get(video_url, stream=True)
        with open("background_video.mp4", "wb") as f:
            f.write(video_response.content)

        audio_response = requests.get(audio_url)
        with open("quran_recitation.mp3", "wb") as f:
            f.write(audio_response.content)

        # إعداد النصوص
        font_url = "https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf"
        font_response = requests.get(font_url)
        with open("Amiri-Regular.ttf", "wb") as f:
            f.write(font_response.content)
        font = ImageFont.truetype("Amiri-Regular.ttf", size=80)

        def create_text_overlay(text, font, size):
            overlay = Image.new("RGBA", size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
            x = (size[0] - text_width) // 2
            y = (size[1] - text_height) // 2
            draw.text((x, y), text, font=font, fill="white")
            return np.array(overlay)

        video_clip = VideoFileClip("background_video.mp4")
        text_overlay = create_text_overlay(quranic_text, font, video_clip.size)
        text_clip = ImageClip(text_overlay).set_duration(video_clip.duration)

        final_video = CompositeVideoClip([video_clip, text_clip])
        final_video = final_video.set_audio(AudioFileClip("quran_recitation.mp3"))
        final_video.write_videofile("final_video_with_audio.mp4", fps=24)

        st.success("تم إنشاء الفيديو بنجاح!")
        st.video("final_video_with_audio.mp4")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")

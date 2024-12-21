
from flask import Flask, request, jsonify
from moviepy.editor import *
import requests
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

# دالة لجلب النصوص القرآنية
def fetch_quran_text(surah, ayah_start, ayah_end):
    url = f"https://api.alquran.cloud/v1/surah/{surah}/ar.alafasy"
    response = requests.get(url).json()
    ayahs = response['data']['ayahs'][ayah_start-1:ayah_end]
    return " ".join([ayah['text'] for ayah in ayahs])

# إعداد النصوص العربية
def prepare_text_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)  # إعادة ترتيب النص
    return get_display(reshaped_text)  # عرض النص بالعربية

# دالة لتوليد الفيديو
def generate_quran_video(output_file, surah, ayah_start, ayah_end):
    # جلب النصوص القرآنية
    quran_text = fetch_quran_text(surah, ayah_start, ayah_end)
    formatted_text = prepare_text_arabic(quran_text)

    # إعداد الخلفية
    clip = ColorClip(size=(1920, 1080), color=(0, 0, 0)).set_duration(30)

    # إعداد النصوص
    text_clip = TextClip(formatted_text, fontsize=70, font="Amiri", color="white", size=(1700, 1000), method='caption')
    text_clip = text_clip.set_position("center").set_duration(30)

    # إضافة صوت تلاوة
    audio_clip = AudioFileClip("alquran_audio.mp3").subclip(0, 30)

    # دمج النصوص والصوت مع الخلفية
    final_clip = CompositeVideoClip([clip, text_clip])
    final_clip = final_clip.set_audio(audio_clip)

    # تصدير الفيديو
    final_clip.write_videofile(output_file, fps=24, codec="libx264")

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    surah = data.get("surah", 1)
    ayah_start = data.get("ayah_start", 1)
    ayah_end = data.get("ayah_end", 7)

    output_file = "quran_video.mp4"
    generate_quran_video(output_file, surah, ayah_start, ayah_end)

    return jsonify({"message": "تم إنشاء الفيديو بنجاح", "video": output_file})

if __name__ == "__main__":
    app.run(debug=True)

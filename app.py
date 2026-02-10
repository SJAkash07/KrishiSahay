import gradio as gr
import google.genai as genai
import tempfile
import re

from gtts import gTTS
from config.config import MODEL_NAME, client
from services.crop_service import retrieve_crop_info
from services.fertilizer_service import retrieve_fertilizer_info
from services.crop_rotation_service import retrieve_crop_rotation_info
from services.location_service import get_location_from_ip
from services.weather_service import get_weather_by_location


# ---------------- Gemini Model ----------------


# ---------------- Language UI Text ----------------
LANG_TEXT = {
    "English": {
        "title": "KrishiSahay 🌾",
        "question_label": "Farmer's Question",
        "question_placeholder": "How should I grow rice?",
        "language_label": "Language",
        "submit": "Submit",
        "missing_crop": "Please mention the crop name so I can help you."
    },
    "Hindi": {
        "title": "कृषि सहाय 🌾",
        "question_label": "किसान का प्रश्न",
        "question_placeholder": "धान की खेती कैसे करें?",
        "language_label": "भाषा",
        "submit": "जमा करें",
        "missing_crop": "कृपया फसल का नाम बताएं ताकि मैं आपकी मदद कर सकूं।"
    }
}


# ---------------- Text → Speech ----------------
def text_to_speech(text, language):
    lang_code = "hi" if language == "Hindi" else "en"
    tts = gTTS(text=text, lang=lang_code)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name


# ---------------- Clean text for audio ----------------
def clean_text_for_audio(text):
    # Replace ranges like "60-75" with "60 to 75"
    text = re.sub(r'(\d+)\s*-\s*(\d+)', r'\1 to \2', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()
    text = re.sub(r"\s+", " ", text)
    text = text.replace("\n", ". ")
    text = text.replace(":", "")
    text = text.replace("–", "")
    return text.strip()


# ---------------- Intent Detection ----------------
def is_weather_question(text):
    keywords = [
        "weather", "rain", "rainfall", "temperature", "climate",
        "forecast", "tomorrow", "next",
        "मौसम", "बारिश", "तापमान", "जलवायु", "कल"
    ]
    return any(k in text.lower() for k in keywords)


def is_planting_question(text):
    keywords = [
        "can i plant", "can i grow", "should i sow",
        "planting", "sowing",
        "क्या मैं बो सकता", "क्या उगाना ठीक है", "बुवाई"
    ]
    return any(k in text.lower() for k in keywords)


# ---------------- Hindi → English (crop detection only) ----------------
def translate_to_english(text):
    prompt = f"""
Translate the following farmer question to simple English.
Only return the translated text.

TEXT:
{text}
"""
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return response.text.strip().lower()


# ---------------- Crop Detection ----------------
def detect_crop_from_text(text, chat_history, language):
    combined_text = text
    for msg in reversed(chat_history):
        if msg["role"] == "user":
            combined_text += " " + msg["content"]

    if language == "Hindi":
        combined_text = translate_to_english(combined_text)

    combined_text = combined_text.lower()

    crops = [
        "rice", "wheat", "maize", "barley", "sorghum",
        "pearl millet", "potato", "banana", "cotton",
        "sugarcane", "groundnut", "mustard",
        "soybean", "tomato", "onion"
    ]

    for crop in crops:
        if crop in combined_text:
            return crop
    return None


# ---------------- Cards ----------------
def format_weather_card(w):
    return f"""
### 🌦️ Current Weather

📍 **Location:** {w['city']}  
🌡️ **Temperature:** {w['temp']}°C  
💧 **Humidity:** {w['humidity']}%  
💨 **Wind Speed:** {w['wind']} m/s  
🌤️ **Condition:** {w['desc']}
"""


def format_rotation_card(text):
    return f"""
### 🌾 Crop Rotation Advice

{text}
"""


# ---------------- Core Logic ----------------
def krishi_sahay(question, language, chat_history):

    # Initial loading
    yield (
        gr.update(visible=True),
        chat_history,
        None,
        chat_history,
        gr.update(visible=False),
        gr.update(visible=False)
    )

    planting_intent = is_planting_question(question)

    # -------- WEATHER ONLY --------
    if not planting_intent and is_weather_question(question):
        location = get_location_from_ip()
        weather_text, weather_data = None, None

        if location:
            weather_text, weather_data = get_weather_by_location(location, language)

        response_text = weather_text or "Weather data not available."

        chat_history += [
            {"role": "user", "content": question},
            {"role": "assistant", "content": response_text}
        ]

        audio_path = text_to_speech(clean_text_for_audio(response_text), language)

        yield (
            gr.update(visible=False),
            chat_history,
            audio_path,
            chat_history,
            gr.update(value=format_weather_card(weather_data), visible=True)
            if weather_data else gr.update(visible=False),
            gr.update(visible=False)
        )
        return

    # -------- CROP FLOW --------
    crop_name = detect_crop_from_text(question, chat_history, language)

    if not crop_name:
        chat_history += [
            {"role": "user", "content": question},
            {"role": "assistant", "content": LANG_TEXT[language]["missing_crop"]}
        ]

        yield (
            gr.update(visible=False),
            chat_history,
            None,
            chat_history,
            gr.update(visible=False),
            gr.update(visible=False)
        )
        return

    crop_context = retrieve_crop_info(crop_name, language)
    fertilizer_context = retrieve_fertilizer_info(crop_name)
    rotation_context = retrieve_crop_rotation_info(crop_name, language)

    location = get_location_from_ip()
    weather_text, weather_data = None, None
    if location:
        weather_text, weather_data = get_weather_by_location(location, language)

    language_instruction = (
        "Respond in simple Hindi using farmer-friendly language."
        if language == "Hindi"
        else "Respond in simple English using farmer-friendly language."
    )

    prompt = f"""
You are an agricultural assistant for farmers.

LANGUAGE:
{language_instruction}

RULES:
- Give only necessary information
- Keep answer medium length
- Use simple words
- Do NOT greet the user

CROP DATA:
{crop_context}

FERTILIZER DATA:
{fertilizer_context}

WEATHER CONDITIONS:
{weather_text if weather_text else "Weather data not available."}

QUESTION:
{question}
"""

    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    response_text = response.text.strip()

    chat_history += [
        {"role": "user", "content": question},
        {"role": "assistant", "content": response_text}
    ]

    audio_path = text_to_speech(clean_text_for_audio(response_text), language)

    yield (
        gr.update(visible=False),
        chat_history,
        audio_path,
        chat_history,
        gr.update(value=format_weather_card(weather_data), visible=True)
        if weather_data else gr.update(visible=False),
        gr.update(value=format_rotation_card(rotation_context), visible=True)
        if rotation_context else gr.update(visible=False)
    )


# ---------------- UI ----------------
with gr.Blocks() as demo:
    language = gr.Dropdown(
        choices=["English", "Hindi"],
        value="English",
        label=LANG_TEXT["English"]["language_label"]
    )

    title_md = gr.Markdown(f"# {LANG_TEXT['English']['title']}")

    weather_card = gr.Markdown(visible=False)
    rotation_card = gr.Markdown(visible=False)

    question_input = gr.Textbox(
        label=LANG_TEXT["English"]["question_label"],
        placeholder=LANG_TEXT["English"]["question_placeholder"]
    )

    submit = gr.Button(value=LANG_TEXT["English"]["submit"])

    loading_md = gr.Markdown(
        "⏳ **Generating response, please wait...**",
        visible=False
    )

    chatbot = gr.Chatbot(label="KrishiSahay Chat 🌾", height=400)
    output_audio = gr.Audio(label="🔊 Audio Response", autoplay=True)

    chat_state = gr.State([])

    submit.click(
        fn=krishi_sahay,
        inputs=[question_input, language, chat_state],
        outputs=[
            loading_md,
            chatbot,
            output_audio,
            chat_state,
            weather_card,
            rotation_card
        ]
    )

    submit.click(fn=lambda: "", outputs=question_input)

demo.launch()
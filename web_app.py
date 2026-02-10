from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import tempfile
import google.genai as genai
from gtts import gTTS
from config.config import MODEL_NAME, client
from services.crop_service import retrieve_crop_info
from services.fertilizer_service import retrieve_fertilizer_info
from services.crop_rotation_service import retrieve_crop_rotation_info
from services.location_service import get_location_from_ip
from services.weather_service import get_weather_by_location

app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize Gemini using the client from config

# Language text mapping
LANG_TEXT = {
    "English": {
        "title": "KrishiSahay - Your AI Farming Assistant",
        "subtitle": "Powered by Advanced Agriculture AI",
        "question_label": "Farmer's Question",
        "question_placeholder": "Ask me about farming, crops, weather, fertilizers...",
        "language_label": "Language",
        "submit": "Submit",
        "missing_crop": "Please mention the crop name so I can help you.",
        "new_chat": "New Chat",
        "chat_history": "Chat History",
        "settings": "Settings",
        "help": "Help",
        "welcome": "Welcome to KrishiSahay",
        "welcome_desc": "Your AI-Powered Farming Intelligence Assistant",
        "ask_crops": "Ask about crops",
        "ask_crops_desc": "Get expert advice on cultivation",
        "fertilizer_info": "Fertilizer info",
        "fertilizer_desc": "Learn about fertilizers & nutrients",
        "crop_rotation": "Crop rotation",
        "crop_rotation_desc": "Optimize your crop rotation plan",
        "weather_info": "Weather info",
        "weather_desc": "Get local weather insights",
        "send": "Send message (Ctrl+Enter)",
        "press_ctrl": "Press Ctrl+Enter to send",
        "thinking": "KrishiSahay is thinking...",
        "enable_audio": "Enable audio responses",
        "enable_animations": "Enable animations",
        "error": "Error",
        "unknown_error": "Unknown error occurred",
        "request_failed": "Request failed",
        "please_enter": "Please enter a question!"
    },
    "Hindi": {
        "title": "कृषि सहाय - आपका AI कृषि सहायक",
        "subtitle": "उन्नत कृषि AI द्वारा संचालित",
        "question_label": "किसान का प्रश्न",
        "question_placeholder": "मुझसे खेती, फसल, मौसम, उर्वरक के बारे में पूछें...",
        "language_label": "भाषा",
        "submit": "जमा करें",
        "missing_crop": "कृपया फसल का नाम बताएं ताकि मैं आपकी मदद कर सकूं।",
        "new_chat": "नई बातचीत",
        "chat_history": "बातचीत का इतिहास",
        "settings": "सेटिंग्स",
        "help": "मदद",
        "welcome": "कृषि सहाय में आपका स्वागत है",
        "welcome_desc": "आपका AI-संचालित कृषि बुद्धिमत्ता सहायक",
        "ask_crops": "फसलों के बारे में पूछें",
        "ask_crops_desc": "खेती पर विशेषज्ञ सलाह प्राप्त करें",
        "fertilizer_info": "उर्वरक जानकारी",
        "fertilizer_desc": "उर्वरक और पोषक तत्वों के बारे में जानें",
        "crop_rotation": "फसल चक्र",
        "crop_rotation_desc": "अपनी फसल चक्र योजना को अनुकूलित करें",
        "weather_info": "मौसम की जानकारी",
        "weather_desc": "स्थानीय मौसम की जानकारी प्राप्त करें",
        "send": "संदेश भेजें (Ctrl+Enter)",
        "press_ctrl": "भेजने के लिए Ctrl+Enter दबाएं",
        "thinking": "कृषि सहाय सोच रहा है...",
        "enable_audio": "ऑडियो प्रतिक्रिया सक्षम करें",
        "enable_animations": "एनिमेशन सक्षम करें",
        "error": "त्रुटि",
        "unknown_error": "अज्ञात त्रुटि हुई",
        "request_failed": "अनुरोध विफल",
        "please_enter": "कृपया एक प्रश्न दर्ज करें!"
    }
}


import re

def text_to_speech(text, language):
    """Convert text to speech"""
    lang_code = "hi" if language == "Hindi" else "en"
    tts = gTTS(text=text, lang=lang_code)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name


def clean_text_for_audio(text):
    """Clean text for better text-to-speech readability"""
    # Replace ranges like "60-75" with "60 to 75"
    text = re.sub(r'(\d+)\s*-\s*(\d+)', r'\1 to \2', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def match_crop_name(user_crop, candidates):
    """Simple crop name matching"""
    user_crop_lower = user_crop.lower()
    for candidate in candidates:
        if user_crop_lower in candidate.lower() or candidate.lower() in user_crop_lower:
            return candidate
    return None


def get_crop_info_for_model(crop, language):
    """Get crop information to provide context to the model"""
    crop_info = retrieve_crop_info(crop, language)
    fertilizer_info = retrieve_fertilizer_info(crop)
    rotation_info = retrieve_crop_rotation_info(crop, language)
    
    context = f"""
    Crop Information for {crop}:
    Basic Info: {crop_info}
    Fertilizer Requirements: {fertilizer_info}
    Crop Rotation Tips: {rotation_info}
    """
    return context


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """API endpoint to process farmer questions"""
    try:
        data = request.json
        question = data.get('question', '').strip()
        language = data.get('language', 'English')
        chat_history = data.get('chat_history', [])
        
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        # Build conversation context from chat history
        conversation_context = ""
        if chat_history:
            conversation_context = "Previous conversation:\n"
            for msg in chat_history[:-1]:  # Exclude the current question
                role = "Farmer" if msg['type'] == 'user' else "KrishiSahay Assistant"
                conversation_context += f"{role}: {msg['content']}\n\n"
        
        # Simple crop detection
        crop_found = None
        crop_context = ""
        for word in question.split():
            try:
                crop_info = retrieve_crop_info(word.lower(), language)
                if crop_info:
                    crop_found = word.lower()
                    crop_context = get_crop_info_for_model(crop_found, language)
                    break
            except:
                pass
        
        # Get weather data
        user_location = get_location_from_ip()
        weather_data = get_weather_by_location(user_location, language)
        
        # Create prompt for Gemini with conversation context
        if crop_context:
            prompt = f"""
            You are an expert agricultural advisor. Answer questions directly and practically.
            
            {conversation_context}
            
            Crop Information: {crop_context}
            
            Current Weather: {weather_data}
            
            Farmer's Question: {question}
            
            LANGUAGE: You MUST respond ONLY in {language}. Do not mix languages. Every word must be in {language}.
            
            INSTRUCTIONS:
            - Provide direct, practical advice without any greetings or flowery language.
            - Do not start with "Namaste", "Hello", or any cultural greetings.
            - Write in simple, easy-to-understand language.
            - Format as continuous paragraphs without bullet points.
            - This will be converted to audio, so keep it natural and conversational.
            - Reference previous conversation if relevant to maintain context.
            - Keep response to 2-3 paragraphs maximum.
            """
        else:
            prompt = f"""
            You are an expert agricultural advisor. Answer questions directly and practically.
            
            {conversation_context}
            
            Current Location Weather: {weather_data}
            
            Farmer's Question: {question}
            
            LANGUAGE: You MUST respond ONLY in {language}. Do not mix languages. Every word must be in {language}.
            
            INSTRUCTIONS:
            - Provide direct, practical advice without any greetings or flowery language.
            - Do not start with "Namaste", "Hello", or any cultural greetings.
            - Write in simple, easy-to-understand language.
            - Format as continuous paragraphs without bullet points.
            - This will be converted to audio, so keep it natural and conversational.
            - Reference previous conversation if relevant to maintain context.
            - Keep response to 2-3 paragraphs maximum.
            """
        
        # Get response from Gemini
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        answer = response.text
        
        # Clean text for audio
        cleaned_answer = clean_text_for_audio(answer)
        
        # Generate audio
        audio_file = text_to_speech(cleaned_answer, language)
        
        return jsonify({
            'answer': answer,
            'audio_url': f'/audio/{os.path.basename(audio_file)}'
        })
    
    except Exception as e:
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500



@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve audio files"""
    return send_from_directory(tempfile.gettempdir(), filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

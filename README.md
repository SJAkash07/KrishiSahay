
# 🌾 KRISHISAHAY – AI-Powered Farmer Assistant

KrishiSahay is a multilingual, AI-powered agricultural assistant designed to help farmers with crop guidance, fertilizer recommendations, crop rotation planning, and real-time weather updates.  
The system supports English and Hindi, includes voice responses, and uses live data with AI reasoning for practical farming decisions.

---

## 🚀 Features

- 🌱 Crop cultivation guidance  
- 🧪 Fertilizer recommendations  
- 🌾 Crop rotation advice  
- 🌦️ Location-based real-time weather updates  
- 🗣️ Text-to-Speech (TTS) responses  
- 🌐 English & Hindi language support  
- 📊 PostgreSQL database-driven recommendations  
- 🤖 Google Gemini AI integration  
- 🎨 Custom HTML, CSS & JavaScript frontend  

---

## 🛠️ Tech Stack

### Backend
- Python
- Gradio
- Google Gemini API
- PostgreSQL (Neon DB)
- OpenWeatherMap API
- gTTS (Text-to-Speech)

### Frontend
- HTML
- CSS
- JavaScript

---

## 📁 Project Structure

```
KRISHISAHAY/
│
├── app.py                     # Gradio-based application
├── web_app.py                 # Web application entry
│
├── config/
│   └── __init__.py
│
├── services/
│   ├── __init__.py
│   ├── crop_service.py
│   ├── fertilizer_service.py
│   ├── crop_rotation_service.py
│   ├── soil_service.py
│   └── weather_service.py
│
├── utils/
│   ├── __init__.py
│   └── data_loader.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── .env
├── .gitignore
├── requirements.txt
├── test.py
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone <your-repository-url>
cd KRISHISAHAY
```

---

### 2️⃣ Create & Activate Virtual Environment (Recommended)

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

## 🔐 Environment Variables Setup

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
DATABASE_URL=postgresql://neondb_owner:npg_Kw2D1LSuZTFf@ep-crimson-field-airuyid2-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

### 🔑 Gemini API Key
Get your API key from: https://aistudio.google.com/app/apikey

### 🌦️ Weather API Key
Get your API key from: https://openweathermap.org/api

### 🗄️ Database
This project uses a cloud-hosted PostgreSQL database on Neon.  
No local database setup is required.

Required tables:
- crops
- fertilizers
- crop_rotation_plan

---

## ▶️ Running the Applications

### Run Gradio App
```bash
python app.py
```

Gradio will start at:
```
http://127.0.0.1:7860
```

---

### Run Web Application
```bash
python web_app.py
```

The web application will start on the configured local server (check terminal output).

---

## 🎨 Frontend Files

- `templates/index.html` – Base HTML layout
- `static/style.css` – Styling
- `static/script.js` – Client-side logic

---

## 🔊 Text-to-Speech Support

If audio is not working:
```bash
python -m pip install gTTS
```

The application continues to work even if TTS is unavailable.

---

## 🧪 Example Questions

- How should I grow rice?
- Which fertilizer is best for wheat?
- Can I plant tomato now?
- आज का मौसम कैसा है?
- धान के बाद कौन सी फसल लगाएं?

---

## 🌱 Future Enhancements

- Crop disease detection
- Image-based crop diagnosis
- Offline voice support
- Regional language expansion
- Cost–benefit fertilizer analysis

---

## 🏆 Hackathon Note

KrishiSahay is built as a real-world, scalable agricultural assistant focusing on accessibility, AI + database integration, and farmer-centric decision making.

---

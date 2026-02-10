from config.database import get_connection

# Fallback crop data
FALLBACK_CROPS = {
    "rice": {
        "name": "Rice",
        "name_hi": "धान",
        "type": "Cereal",
        "description": "Rice is a staple crop requiring warm temperatures and adequate water. Plant in monsoon season.",
        "description_hi": "धान एक मुख्य फसल है जिसे गर्म तापमान और पर्याप्त पानी की आवश्यकता होती है। मानसून में लगाएं।",
        "climate": "Tropical, Subtropical",
        "soil": "Clay, Loamy soil with good water retention",
        "temp": "20-30°C",
        "water": "1000-1500 mm",
        "season": "June-October",
        "price": 50
    },
    "wheat": {
        "name": "Wheat",
        "name_hi": "गेहूं",
        "type": "Cereal",
        "description": "Wheat thrives in cool seasons with moderate rainfall. Plant in October-November.",
        "description_hi": "गेहूं ठंडे मौसम में अच्छी तरह उगता है। अक्टूबर-नवंबर में लगाएं।",
        "climate": "Temperate",
        "soil": "Well-drained loamy soil",
        "temp": "15-25°C",
        "water": "400-500 mm",
        "season": "October-March",
        "price": 25
    },
    "maize": {
        "name": "Maize",
        "name_hi": "मक्का",
        "type": "Cereal",
        "description": "Maize is a summer crop that requires warm temperatures and good moisture.",
        "description_hi": "मक्का एक गर्मी की फसल है जिसे गर्म तापमान की आवश्यकता होती है।",
        "climate": "Tropical, Subtropical",
        "soil": "Well-drained loamy soil",
        "temp": "21-27°C",
        "water": "500-750 mm",
        "season": "May-September",
        "price": 20
    },
    "cotton": {
        "name": "Cotton",
        "name_hi": "कपास",
        "type": "Cash Crop",
        "description": "Cotton requires warm climate, good drainage, and moderate rainfall.",
        "description_hi": "कपास को गर्म जलवायु और अच्छी जल निकासी की आवश्यकता होती है।",
        "climate": "Tropical, Subtropical",
        "soil": "Well-drained loamy soil",
        "temp": "21-30°C",
        "water": "600-900 mm",
        "season": "June-October",
        "price": 5500
    },
    "sugarcane": {
        "name": "Sugarcane",
        "name_hi": "गन्ना",
        "type": "Cash Crop",
        "description": "Sugarcane is a long-duration crop requiring warm temperature and ample water.",
        "description_hi": "गन्ना एक लंबी अवधि की फसल है जिसे गर्म तापमान और पर्याप्त पानी चाहिए।",
        "climate": "Tropical, Subtropical",
        "soil": "Deep loamy soil",
        "temp": "21-27°C",
        "water": "2000-2250 mm",
        "season": "November-December planting",
        "price": 40
    }
}

def retrieve_crop_info(crop_name, language):
    try:
        conn = get_connection()
        cur = conn.cursor()

        if language == "Hindi":
            cur.execute("""
                SELECT
                    crop_name_hi,
                    crop_type,
                    description_hi,
                    suitable_climate,
                    suitable_soil,
                    ideal_temperature_celsius,
                    water_requirement,
                    growing_season,
                    price_per_kg_inr
                FROM crops
                WHERE lower(crop_name) = %s
            """, (crop_name.lower(),))
        else:
            cur.execute("""
                SELECT
                    crop_name,
                    crop_type,
                    description,
                    suitable_climate,
                    suitable_soil,
                    ideal_temperature_celsius,
                    water_requirement,
                    growing_season,
                    price_per_kg_inr
                FROM crops
                WHERE lower(crop_name) = %s
            """, (crop_name.lower(),))

        row = cur.fetchone()
        conn.close()
        
        if row:
            return row
    except Exception as e:
        print(f"Database error: {e}. Using fallback data.")
    
    # Fallback to local data
    crop_lower = crop_name.lower()
    if crop_lower in FALLBACK_CROPS:
        crop = FALLBACK_CROPS[crop_lower]
        if language == "Hindi":
            return (crop["name_hi"], crop["type"], crop["description_hi"], 
                   crop["climate"], crop["soil"], crop["temp"], 
                   crop["water"], crop["season"], crop["price"])
        else:
            return (crop["name"], crop["type"], crop["description"],
                   crop["climate"], crop["soil"], crop["temp"],
                   crop["water"], crop["season"], crop["price"])

    if not row:
        return None

    if language == "Hindi":
        return f"""
फसल: {row[0]}
फसल प्रकार: {row[1]}
विवरण: {row[2]}
उपयुक्त जलवायु: {row[3]}
उपयुक्त मिट्टी: {row[4]}
आदर्श तापमान (°C): {row[5]}
पानी की आवश्यकता: {row[6]}
उगाने का मौसम: {row[7]}
बाज़ार मूल्य (₹/किलो): {row[8]}
"""
    else:
        return f"""
Crop: {row[0]}
Crop type: {row[1]}
Description: {row[2]}
Suitable climate: {row[3]}
Suitable soil: {row[4]}
Ideal temperature (°C): {row[5]}
Water requirement: {row[6]}
Growing season: {row[7]}
Market price (₹/kg): {row[8]}
"""

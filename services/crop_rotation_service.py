from config.database import get_connection

# Fallback crop rotation data
FALLBACK_ROTATIONS = {
    "rice": [
        {
            "next_crop": "Wheat",
            "next_crop_hi": "गेहूं",
            "season": "Rabi (October-March)",
            "reason": "Wheat is grown in winter after rice, utilizing residual moisture.",
            "soil_effect": "Improves soil structure and nitrogen availability.",
            "pest_benefit": "Breaks pest and disease cycle of rice.",
            "gap_days": 30,
            "precautions": "Proper rice straw management required."
        }
    ],
    "wheat": [
        {
            "next_crop": "Rice",
            "next_crop_hi": "धान",
            "season": "Kharif (June-October)",
            "reason": "Rice is ideal summer crop after wheat.",
            "soil_effect": "Maintains soil fertility through legume rotation.",
            "pest_benefit": "Breaks wheat pest cycle effectively.",
            "gap_days": 30,
            "precautions": "Prepare land adequately with irrigation."
        }
    ],
    "cotton": [
        {
            "next_crop": "Pulses (Chickpea/Gram)",
            "next_crop_hi": "दालें (चना)",
            "season": "Rabi (October-February)",
            "reason": "Legumes improve soil nitrogen after cotton.",
            "soil_effect": "Greatly improves soil nitrogen levels.",
            "pest_benefit": "Breaks cotton pest and disease cycle.",
            "gap_days": 30,
            "precautions": "Ensure proper spacing for chickpea."
        }
    ],
    "maize": [
        {
            "next_crop": "Legumes/Pulses",
            "next_crop_hi": "दालें",
            "season": "Rabi/Kharif",
            "reason": "Legumes restore nitrogen depleted by maize.",
            "soil_effect": "Nitrogen fixation improves soil health.",
            "pest_benefit": "Reduces maize pest populations.",
            "gap_days": 15,
            "precautions": "Adequate moisture needed for legume germination."
        }
    ]
}

def retrieve_crop_rotation_info(crop_name, language):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # First get crop_id of current crop
        cur.execute("""
            SELECT crop_id
            FROM crops
            WHERE lower(crop_name) = %s
        """, (crop_name.lower(),))

        row = cur.fetchone()
        if not row:
            conn.close()
            raise Exception("Crop not found in database")

        crop_id = row[0]

        # Get rotation info
        cur.execute("""
            SELECT
                c2.crop_name,
                c2.crop_name_hi,
                r.recommended_season,
                r.rotation_reason,
                r.soil_nutrient_effect,
                r.pest_disease_benefit,
                r.recommended_gap_days,
                r.special_precautions
            FROM public.crop_rotation_plan r
            JOIN crops c2 ON r.next_crop_id = c2.crop_id
            WHERE r.current_crop_id = %s
        """, (crop_id,))

        rows = cur.fetchall()
        conn.close()

        if rows:
            if language == "Hindi":
                return "\n".join(
                    f"""
अगली फसल: {r[1]}
मौसम: {r[2]}
कारण: {r[3]}
मिट्टी पर प्रभाव: {r[4]}
कीट/रोग लाभ: {r[5]}
अंतराल (दिन): {r[6]}
सावधानियाँ: {r[7]}
"""
                    for r in rows
                )
            else:
                return "\n".join(
                    f"""
Next crop: {r[0]}
Season: {r[2]}
Reason: {r[3]}
Soil effect: {r[4]}
Pest/Disease benefit: {r[5]}
Gap (days): {r[6]}
Precautions: {r[7]}
"""
                    for r in rows
                )
    except Exception as e:
        print(f"Database error: {e}. Using fallback data.")
    
    # Fallback to local data
    crop_lower = crop_name.lower()
    if crop_lower in FALLBACK_ROTATIONS:
        rotations = FALLBACK_ROTATIONS[crop_lower]
        if language == "Hindi":
            return "\n".join(
                f"""
अगली फसल: {r['next_crop_hi']}
मौसम: {r['season']}
कारण: {r['reason']}
मिट्टी पर प्रभाव: {r['soil_effect']}
कीट/रोग लाभ: {r['pest_benefit']}
अंतराल (दिन): {r['gap_days']}
सावधानियाँ: {r['precautions']}
"""
                for r in rotations
            )
        else:
            return "\n".join(
                f"""
Next crop: {r['next_crop']}
Season: {r['season']}
Reason: {r['reason']}
Soil effect: {r['soil_effect']}
Pest/Disease benefit: {r['pest_benefit']}
Gap (days): {r['gap_days']}
Precautions: {r['precautions']}
"""
                for r in rotations
            )
    
    return "No crop rotation data available."

from config.database import get_connection

# Fallback fertilizer data
FALLBACK_FERTILIZERS = {
    "rice": "For rice, use Urea (Nitrogen-rich) at 120-150 kg/hectare during growing season. Apply Phosphate (DAP) 60-80 kg/hectare at planting and Potash 40-60 kg/hectare for better yields.",
    "wheat": "For wheat, apply Urea 120 kg/hectare in splits - half at planting and half at tillering stage. Use DAP 80 kg/hectare at planting. Potash application 40 kg/hectare improves grain quality.",
    "maize": "For maize, apply Urea 150 kg/hectare in splits and DAP 100 kg/hectare at planting. Micronutrients like Zinc and Boron are beneficial for higher yields.",
    "cotton": "For cotton, use Urea 180 kg/hectare, DAP 100 kg/hectare, and Potash 60 kg/hectare. Split applications are recommended for better growth.",
    "sugarcane": "For sugarcane, apply high doses of Nitrogen (200-250 kg/hectare) and Phosphate (100-120 kg/hectare). FYM 25-30 tons/hectare improves soil health."
}

def retrieve_fertilizer_info(crop_name):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                fertilizer_name,
                type,
                nutrients,
                application_stage,
                price_per_kg_inr
            FROM fertilizers
            WHERE lower(used_for_crops) LIKE %s
        """, (f"%{crop_name.lower()}%",))

        rows = cur.fetchall()
        conn.close()

        if rows:
            return "\n".join(
                f"- {r[0]} ({r[1]}): Nutrients: {r[2]}, "
                f"Stage: {r[3]}, Price: ₹{r[4]}/kg"
                for r in rows
            )
    except Exception as e:
        print(f"Database error: {e}. Using fallback data.")
    
    # Fallback to local data
    crop_lower = crop_name.lower()
    if crop_lower in FALLBACK_FERTILIZERS:
        return FALLBACK_FERTILIZERS[crop_lower]
    
    return "No specific fertilizer data available."

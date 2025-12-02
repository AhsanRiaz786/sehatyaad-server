import google.generativeai as genai
from config import Config
import base64
import logging

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro')

GEMINI_PROMPT = """
You are an expert medical prescription analyzer with deep knowledge of:
- Common medication names and their variants
- Standard dosage formats and units  
- Prescription abbreviations (Latin and common)
- Typical prescription layouts

TASK: Extract structured medication data from this prescription image.

IMPORTANT CONTEXT:
- Prescriptions may be handwritten or printed
- Common abbreviations to recognize:
  * Dosing: OD/QD(once), BID/BD(twice), TID/TD(3x), QID(4x), PRN(as needed)
  * Units: mg(milligram), ml(milliliter), IU(units), mcg(microgram), gm(gram), tab(tablet), cap(capsule)
  * Routes: PO(oral), IV(intravenous), IM(intramuscular), TOP(topical)
  * Timing: HS(bedtime), AC(before meals), PC(after meals), STAT(immediately)

EXTRACTION RULES:
1. Medication Name: Use generic name if available, otherwise brand name
2. Dosage: Extract numeric value only (without unit)
3. Dosage Unit: Extract unit separately (mg, ml, IU, tab, cap, etc.)
4. Frequency: Convert ALL abbreviations to plain English:
   - "OD"/"QD"/"Once" → "once daily"
   - "BID"/"BD"/"Twice" → "twice daily"
   - "TID"/"TD" → "three times daily"
   - "QID" → "four times daily"
   - "HS" → "at bedtime"
   - "PRN" → "as needed"
5. Times: Suggest appropriate times based on frequency:
   - once daily → ["08:00"]
   - twice daily → ["08:00", "20:00"]
   - three times daily → ["08:00", "14:00", "20:00"]
   - four times daily → ["08:00", "12:00", "16:00", "20:00"]
   - at bedtime → ["22:00"]
6. Instructions: Extract any special notes (with food, avoid alcohol, etc.)
7. Confidence: 
   - "high" if text is very clear and complete
   - "medium" if readable but some uncertainty
   - "low" if hard to read or incomplete

OUTPUT FORMAT (JSON only, NO markdown, NO explanations):
{
  "medications": [
    {
      "name": "medication name",
      "dosage": "100",
      "dosageUnit": "mg",
      "frequency": "once daily",
      "times": ["08:00"],
      "instructions": "take with food",
      "confidence": "high"
    }
  ],
  "doctorName": "Dr. Name (if visible)",
  "date": "YYYY-MM-DD (if visible)",
  "pharmacyName": "Pharmacy name (if visible)"
}

CRITICAL: Return ONLY valid JSON. No markdown code blocks, no extra text.

Now analyze this prescription image carefully:
"""


async def process_prescription_image(image_data: bytes, mime_type: str = 'image/jpeg'):
    """
    Process a prescription image using Gemini AI
    
    Args:
        image_data: Raw image bytes
        mime_type: MIME type of the image
        
    Returns:
        dict: Extracted prescription data
        
    Raises:
        Exception: If processing fails
    """
    try:
        logger.info("🔄 Processing prescription image with Gemini AI...")
        
        # Convert to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Prepare image part for Gemini
        image_part = {
            'inline_data': {
                'data': base64_image,
                'mime_type': mime_type
            }
        }
        
        # Call Gemini API
        logger.info("📡 Calling Gemini API...")
        response = model.generate_content([GEMINI_PROMPT, image_part])
        text = response.text
        
        logger.info("✅ Gemini response received")
        logger.debug(f"📝 Raw response: {text[:200]}...")
        
        # Parse JSON response (remove markdown if present)
        json_text = text.replace('```json\n', '').replace('```\n', '').replace('```', '').strip()
        
        import json
        data = json.loads(json_text)
        
        logger.info(f"✅ Extracted {len(data.get('medications', []))} medications")
        
        # Validate that we have at least some data
        if not data.get('medications') or len(data['medications']) == 0:
            logger.warning('⚠️ No medications extracted from prescription')
            raise ValueError('No medications found in the image')
        
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON parsing failed: {e}")
        raise ValueError(f'Failed to parse Gemini response: {str(e)}')
    except Exception as e:
        logger.error(f"❌ Gemini processing error: {e}")
        raise Exception(f'Failed to process prescription: {str(e)}')


def validate_medication_data(medication: dict) -> bool:
    """Validate extracted medication data has required fields"""
    required_fields = ['name', 'dosage', 'frequency', 'times']
    return all(medication.get(field) for field in required_fields) and len(medication.get('times', [])) > 0

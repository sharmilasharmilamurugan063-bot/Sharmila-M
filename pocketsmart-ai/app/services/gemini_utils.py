import json, re
from typing import Optional
from app.config import get_settings
from app.services.catalog import home_candidates, party_candidates, jewelry_candidates

settings=get_settings()

def _client():
    if not settings.gemini_api_key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=settings.gemini_api_key)
    except Exception:
        return None

def _extract_json(text: str):
    text=text.strip()
    if text.startswith("```"):
        text=re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.I|re.S)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match=re.search(r"\{.*\}", text, flags=re.S)
        if match:
            try: return json.loads(match.group(0))
            except json.JSONDecodeError: pass
    return None

def _call(prompt: str, image_bytes: Optional[bytes]=None, mime_type: Optional[str]=None):
    client=_client()
    if not client: return None
    try:
        contents=[prompt]
        if image_bytes and mime_type:
            from google.genai import types
            contents=[types.Part.from_bytes(data=image_bytes, mime_type=mime_type), prompt]
        response=client.models.generate_content(model=settings.gemini_model, contents=contents)
        return _extract_json(response.text or "")
    except Exception:
        return None

def _schema_instruction():
    return '''Return ONLY valid JSON. Schema: {"title":string,"summary":string,"tips":[string],"allocations":object,"recommendations":[{"name":string,"category":string,"platform":string,"price":number,"quantity":number,"reason":string,"url":string}]}. Never invent a product outside the supplied catalog. Never change catalog prices or URLs. Keep total recommendation spend at or below the requested budget.'''

def generate_home(data):
    candidates=home_candidates([x.category for x in data.items], data.style)
    catalog=candidates[:10]
    prompt=f'''You are PocketSmart AI's home budget planner. Budget: INR {data.budget:.2f}. Rooms: {data.rooms}. Style: {data.style}. Items: {[x.model_dump() for x in data.items]}. Notes: {data.notes}. Catalog: {json.dumps(catalog)}. {_schema_instruction()} Allocate budget by room/item and choose useful quantities. Keep the result realistic.'''
    return _call(prompt), catalog

def generate_party(data):
    catalog=party_candidates(data.event_type)[:10]
    prompt=f'''You are PocketSmart AI's party budget planner. Budget: INR {data.budget:.2f}. Guests: {data.guests}. Event: {data.event_type}. Venue: {data.venue}. City: {data.city}. Notes: {data.notes}. Catalog: {json.dumps(catalog)}. {_schema_instruction()} For per-guest catering, multiply unit price by guest count. Allocate across catering, decoration and optional stay.'''
    return _call(prompt), catalog

def generate_jewelry(data, image_bytes=None, mime_type=None):
    catalog=jewelry_candidates(data["occasion"], data["style"])[:10]
    prompt=f'''You are PocketSmart AI's jewelry planner. Budget: INR {data["budget"]:.2f}. Occasion: {data["occasion"]}. Style: {data["style"]}. Outfit notes: {data.get("outfit_notes","")}. Catalog: {json.dumps(catalog)}. {_schema_instruction()} If an outfit image is supplied, use only broad visual observations such as dominant colors and formality; do not identify the person.'''
    return _call(prompt, image_bytes, mime_type), catalog

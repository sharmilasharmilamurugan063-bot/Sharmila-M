from urllib.parse import quote_plus

PLATFORMS = {
    "Amazon": "https://www.amazon.in/s?k=",
    "Flipkart": "https://www.flipkart.com/search?q=",
    "IKEA": "https://www.ikea.com/in/en/search/?q=",
    "Swiggy": "https://www.swiggy.com/search?query=",
    "Zomato": "https://www.zomato.com/search?q=",
    "OYO": "https://www.oyorooms.com/search?location=",
}


def product_url(platform: str, query: str) -> str:
    base = PLATFORMS.get(platform, PLATFORMS["Amazon"])
    return base + quote_plus(query)


def fallback_home(data: dict) -> dict:
    budget = float(data["budget"])
    alloc = {"furniture": round(budget * .40, 2), "lighting": round(budget * .20, 2), "decor": round(budget * .20, 2), "dining": round(budget * .20, 2)}
    items = [
        ("LED ceiling light", "lighting", alloc["lighting"] * .35, "Amazon", "Energy-efficient lighting that suits the selected rooms."),
        ("Ceiling fan", "lighting", alloc["lighting"] * .45, "Flipkart", "A practical comfort upgrade within the lighting allocation."),
        ("Compact storage cabinet", "furniture", alloc["furniture"] * .55, "IKEA", "Useful storage with a clean look for compact spaces."),
        ("Accent wall art set", "decor", alloc["decor"] * .45, "Amazon", "Adds personality without using a large share of the budget."),
        ("4-seat dining table", "dining", alloc["dining"] * .70, "IKEA", "Balanced option for everyday family use."),
    ]
    return _response("home", budget, alloc, items, ["Compare dimensions before buying.", "Keep at least 5% of the budget uncommitted for delivery or small extras."])


def fallback_party(data: dict) -> dict:
    budget = float(data["budget"])
    alloc = {"catering": round(budget * .50, 2), "decoration": round(budget * .20, 2), "venue": round(budget * .20, 2), "entertainment": round(budget * .10, 2)}
    per_guest = budget / max(int(data["guests"]), 1)
    items = [
        (f"Catering package for {data['guests']} guests", "catering", alloc["catering"], "Swiggy", f"Designed around about ₹{per_guest:,.0f} per guest."),
        ("Event decoration package", "decoration", alloc["decoration"], "Zomato", "Use a simple theme to protect the food and venue budget."),
        (f"Budget venue shortlist in {data.get('city') or 'your area'}", "venue", alloc["venue"], "OYO", "Useful as a starting point for venue research."),
        ("Music and simple entertainment", "entertainment", alloc["entertainment"], "Amazon", "Keep entertainment lightweight if guest count is high."),
    ]
    return _response("party", budget, alloc, items, ["Confirm taxes, service fees and delivery charges with vendors.", "Finalize the guest list before locking food quantities."])


def fallback_jewelry(data: dict) -> dict:
    budget = float(data["budget"])
    alloc = {"earrings": round(budget * .35, 2), "necklace": round(budget * .40, 2), "bangles": round(budget * .15, 2), "reserve": round(budget * .10, 2)}
    style = data.get("style", "classic")
    items = [
        (f"{style.title()} statement earrings", "earrings", alloc["earrings"], "Amazon", "Easy to match with many outfit colors and occasions."),
        (f"{style.title()} necklace set", "necklace", alloc["necklace"], "Flipkart", "A coordinated centerpiece for the selected occasion."),
        ("Minimal bangle set", "bangles", alloc["bangles"], "Amazon", "Keeps the overall look balanced."),
    ]
    return _response("jewelry", budget, alloc, items, ["Check the outfit neckline before choosing a necklace.", "For an outfit image, use the AI result as style guidance rather than an exact color guarantee."])


def _response(planner, budget, allocation, items, tips):
    return {
        "planner": planner,
        "budget": budget,
        "summary": "Fallback recommendations generated from the requested budget and preferences. Connect Gemini for richer personalization.",
        "allocation": allocation,
        "recommendations": [
            {"title": t, "category": c, "estimated_price": round(p, 2), "platform": platform, "reason": r, "url": product_url(platform, t)}
            for t, c, p, platform, r in items
        ],
        "tips": tips,
        "source": "fallback",
    }

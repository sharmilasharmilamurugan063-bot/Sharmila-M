CATALOG = [
    {"name":"Minimalist 3-Seater Sofa","category":"furniture","planner":"home","platform":"IKEA","price":24999,"tags":["living room","modern","minimalist"],"url":"https://www.ikea.com/"},
    {"name":"LED Ceiling Light 24W","category":"lighting","planner":"home","platform":"Amazon","price":1299,"tags":["living room","bedroom","modern"],"url":"https://www.amazon.in/"},
    {"name":"Ceiling Fan 1200mm","category":"fan","planner":"home","platform":"Flipkart","price":1899,"tags":["living room","bedroom","kitchen"],"url":"https://www.flipkart.com/"},
    {"name":"6-Seater Dining Table","category":"dining","planner":"home","platform":"IKEA","price":15999,"tags":["dining","modern","wood"],"url":"https://www.ikea.com/"},
    {"name":"Queen Storage Bed","category":"bedroom","planner":"home","platform":"Amazon","price":21999,"tags":["bedroom","storage","modern"],"url":"https://www.amazon.in/"},
    {"name":"Wall Art Set of 3","category":"decor","planner":"home","platform":"Flipkart","price":999,"tags":["living room","decor","minimalist"],"url":"https://www.flipkart.com/"},
    {"name":"Indoor Birthday Catering Package","category":"catering","planner":"party","platform":"Zomato","price":450,"unit":"per guest","tags":["birthday","indoor"],"url":"https://www.zomato.com/"},
    {"name":"Party Meal Combo","category":"catering","planner":"party","platform":"Swiggy","price":399,"unit":"per guest","tags":["birthday","corporate","indoor"],"url":"https://www.swiggy.com/"},
    {"name":"Simple Party Decoration Kit","category":"decoration","planner":"party","platform":"Amazon","price":2499,"tags":["birthday","indoor","budget"],"url":"https://www.amazon.in/"},
    {"name":"Premium Event Decoration","category":"decoration","planner":"party","platform":"Flipkart","price":5999,"tags":["wedding","corporate","indoor"],"url":"https://www.flipkart.com/"},
    {"name":"Budget Hotel Room","category":"stay","planner":"party","platform":"OYO","price":1499,"unit":"per room","tags":["birthday","wedding","guest stay"],"url":"https://www.oyorooms.com/"},
    {"name":"Corporate Meeting Stay","category":"stay","planner":"party","platform":"OYO","price":1999,"unit":"per room","tags":["corporate","guest stay"],"url":"https://www.oyorooms.com/"},
    {"name":"Classic Gold-Plated Necklace","category":"necklace","planner":"jewelry","platform":"Amazon","price":1799,"tags":["wedding","traditional","gold","ethnic"],"url":"https://www.amazon.in/"},
    {"name":"Pearl Drop Earrings","category":"earrings","planner":"jewelry","platform":"Flipkart","price":899,"tags":["wedding","formal","elegant","white"],"url":"https://www.flipkart.com/"},
    {"name":"Minimal Silver Bracelet","category":"bracelet","planner":"jewelry","platform":"Amazon","price":1299,"tags":["party","formal","minimal","silver"],"url":"https://www.amazon.in/"},
    {"name":"Statement Kundan Earrings","category":"earrings","planner":"jewelry","platform":"Flipkart","price":1499,"tags":["wedding","traditional","kundan","festive"],"url":"https://www.flipkart.com/"},
    {"name":"Rose-Gold Pendant Set","category":"set","planner":"jewelry","platform":"Amazon","price":2299,"tags":["party","modern","pink","rose gold"],"url":"https://www.amazon.in/"},
]

def home_candidates(categories=None, style="modern"):
    categories = {c.lower() for c in (categories or [])}
    scored=[]
    for p in CATALOG:
        if p["planner"] != "home": continue
        score = (2 if p["category"] in categories else 0) + (1 if style.lower() in p["tags"] else 0)
        scored.append((score,p))
    return [p for _,p in sorted(scored,key=lambda x:(x[0],-x[1]["price"]),reverse=True)]

def party_candidates(event_type):
    tag=event_type.lower()
    return sorted([p for p in CATALOG if p["planner"]=="party"], key=lambda p: (tag not in p["tags"], p["price"]))

def jewelry_candidates(occasion, style=""):
    tags=(occasion+" "+style).lower()
    return sorted([p for p in CATALOG if p["planner"]=="jewelry"], key=lambda p: (not any(t in tags for t in p["tags"]), p["price"]))

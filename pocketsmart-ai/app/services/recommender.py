from app.services.catalog import home_candidates, party_candidates, jewelry_candidates

def _item(p, qty, reason):
    return {"name":p["name"],"category":p["category"],"platform":p["platform"],"price":float(p["price"]),"quantity":int(qty),"reason":reason,"url":p["url"]}

def home_fallback(data):
    candidates=home_candidates([x.category for x in data.items], data.style)
    remaining=data.budget
    out=[]
    wanted=[x.model_dump() for x in data.items]
    for w in wanted:
        match=next((p for p in candidates if p["category"]==w["category"]), None)
        if not match: continue
        qty=min(w["quantity"], int(remaining//match["price"]))
        if qty>0:
            out.append(_item(match,qty,f"Fits your {data.style} style and requested {w['category']} quantity.")); remaining-=qty*match["price"]
    for p in candidates:
        if remaining < p["price"] or len(out)>=8: continue
        if not any(x["name"]==p["name"] for x in out):
            out.append(_item(p,1,"Budget-friendly addition selected from the available catalog.")); remaining-=p["price"]
    return {"title":"Home plan","summary":f"A {data.style} home setup prioritized around your requested rooms and items.","tips":["Measure spaces before buying large furniture.","Keep a small contingency for installation and delivery."],"allocations":{"furniture":round(data.budget*.45,2),"lighting":round(data.budget*.15,2),"decor":round(data.budget*.15,2),"other":round(data.budget*.25,2)},"recommendations":out}

def party_fallback(data):
    candidates=party_candidates(data.event_type)
    out=[]; remaining=data.budget
    catering=next(p for p in candidates if p["category"]=="catering")
    qty_cost=catering["price"]*data.guests
    if qty_cost<=remaining:
        out.append(_item(catering,data.guests,f"Catering estimated for {data.guests} guests.")); remaining-=qty_cost
    deco=next(p for p in candidates if p["category"]=="decoration")
    if deco["price"]<=remaining:
        out.append(_item(deco,1,"Decoration allocation matched to the event type.")); remaining-=deco["price"]
    if len(out)<3:
        stay=next(p for p in candidates if p["category"]=="stay")
        if stay["price"]<=remaining:
            out.append(_item(stay,1,"Optional guest accommodation item.")); remaining-=stay["price"]
    return {"title":f"{data.event_type.title()} party plan","summary":f"A starter plan for {data.guests} guests with catering and decoration prioritized.","tips":["Confirm vendor availability before paying.","Keep 10% of the budget as an event-day buffer."],"allocations":{"catering":round(data.budget*.55,2),"decoration":round(data.budget*.25,2),"buffer":round(data.budget*.20,2)},"recommendations":out}

def jewelry_fallback(data):
    candidates=jewelry_candidates(data["occasion"], data["style"])
    out=[]; remaining=data["budget"]
    for p in candidates:
        if p["price"]<=remaining and len(out)<4:
            out.append(_item(p,1,f"Matches the {data['occasion']} occasion and your {data['style']} preference.")); remaining-=p["price"]
    return {"title":"Jewelry style plan","summary":f"A curated {data['occasion']} jewelry shortlist within budget.","tips":["Match metal tone with your outfit accessories.","For statement pieces, keep the rest of the jewelry simple."],"allocations":{"primary":round(data["budget"]*.6,2),"secondary":round(data["budget"]*.25,2),"buffer":round(data["budget"]*.15,2)},"recommendations":out}

def normalize_ai(result, budget):
    if not result or not isinstance(result,dict): return None
    recs=[]
    for r in result.get("recommendations",[]):
        try:
            price=float(r["price"]); qty=max(1,int(r.get("quantity",1)))
            recs.append({"name":str(r["name"]),"category":str(r.get("category","general")),"platform":str(r.get("platform","Catalog")),"price":price,"quantity":qty,"reason":str(r.get("reason","AI-selected recommendation.")),"url":str(r.get("url","#"))})
        except (KeyError,TypeError,ValueError): continue
    total=sum(x["price"]*x["quantity"] for x in recs)
    if total>budget and total:
        # Drop most expensive entries until the total is inside budget.
        recs.sort(key=lambda x:x["price"]*x["quantity"])
        kept=[]; running=0
        for x in recs:
            cost=x["price"]*x["quantity"]
            if running+cost<=budget: kept.append(x); running+=cost
        recs=kept; total=running
    return {"title":str(result.get("title","PocketSmart plan")),"summary":str(result.get("summary","AI-generated plan.")),"tips":list(result.get("tips",[]))[:6],"allocations":result.get("allocations",{}),"recommendations":recs}

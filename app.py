import streamlit as st
import requests
import urllib.parse

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PricePulse",
    page_icon="🔍",
    layout="wide",
)

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0e0e0e;
    color: #f0f0f0;
}

.stApp { background: #0e0e0e; }

h1, h2, h3 { font-family: 'Space Mono', monospace; }

.header-block {
    border: 2px solid #f0f0f0;
    padding: 2rem 2.5rem;
    margin-bottom: 2.5rem;
    position: relative;
}
.header-block::before {
    content: '';
    position: absolute;
    top: 6px; left: 6px;
    right: -6px; bottom: -6px;
    border: 2px solid #c8ff00;
    z-index: -1;
}
.header-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: -1px;
    margin: 0;
    line-height: 1;
}
.header-sub {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    color: #888;
    margin-top: 0.5rem;
    font-size: 1rem;
}

.mode-pill {
    display: inline-block;
    border: 1px solid #333;
    padding: 4px 12px;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #c8ff00;
    margin-bottom: 1.5rem;
    letter-spacing: 1px;
}

.product-card {
    background: #161616;
    border: 1px solid #2a2a2a;
    border-left: 3px solid #c8ff00;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
    position: relative;
}
.product-card:hover { border-left-color: #fff; }

.card-title {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 1rem;
    color: #f0f0f0;
    margin-bottom: 0.75rem;
    line-height: 1.4;
}
.card-price {
    font-family: 'Space Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: #c8ff00;
}
.card-original {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #555;
    text-decoration: line-through;
    margin-left: 0.5rem;
}
.card-discount {
    background: #c8ff00;
    color: #0e0e0e;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 8px;
    margin-left: 0.5rem;
    letter-spacing: 1px;
}
.card-meta {
    display: flex;
    gap: 1.5rem;
    margin-top: 0.75rem;
    flex-wrap: wrap;
}
.meta-item {
    font-size: 0.8rem;
    color: #888;
    font-family: 'DM Sans', sans-serif;
}
.meta-label {
    color: #555;
    margin-right: 4px;
}
.meta-val { color: #ccc; }
.rating-stars { color: #c8ff00; }

.card-source {
    position: absolute;
    top: 1.25rem;
    right: 1.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #444;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.card-link {
    display: inline-block;
    margin-top: 0.75rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #555;
    text-decoration: none;
    border-bottom: 1px solid #333;
    padding-bottom: 1px;
    transition: color 0.2s, border-color 0.2s;
}
.card-link:hover { color: #c8ff00; border-color: #c8ff00; }

.no-results {
    border: 1px dashed #333;
    padding: 3rem;
    text-align: center;
    color: #444;
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
}

.api-warning {
    border: 1px solid #333;
    border-left: 3px solid #ff6b6b;
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
    font-size: 0.85rem;
    color: #888;
    background: #161616;
}
.api-warning a { color: #c8ff00; }

.results-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #444;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.25rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #1e1e1e;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 1px !important;
    color: #666 !important;
    text-transform: uppercase !important;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #161616 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 0 !important;
    color: #f0f0f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stButton > button {
    background: #c8ff00 !important;
    color: #0e0e0e !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    letter-spacing: 1px !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stRadio > div { gap: 0.5rem; }
.stRadio label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-block">
    <p class="header-title">PRICE<br>PULSE</p>
    <p class="header-sub">real-time product price comparison across the web</p>
</div>
""", unsafe_allow_html=True)

# ── API Key input ─────────────────────────────────────────────────────────────
with st.expander("⚙️  Setup — SerpAPI Key (free tier: 100 searches/month)"):
    st.markdown("""
    <div class="api-warning">
    Get a free key at <a href="https://serpapi.com" target="_blank">serpapi.com</a> → 100 free searches/month, no credit card.
    Paste it below. It stays in your browser session only.
    </div>
    """, unsafe_allow_html=True)
    api_key = st.text_input("SerpAPI Key", type="password", placeholder="paste key here...")

# ── Mode selector ─────────────────────────────────────────────────────────────
st.markdown('<div class="mode-pill">// SELECT MODE</div>', unsafe_allow_html=True)
mode = st.radio(
    "",
    ["🔎  Search specific model", "📦  Browse category by budget"],
    horizontal=True,
    label_visibility="collapsed"
)

# ── Search logic ──────────────────────────────────────────────────────────────
def fetch_shopping_results(query: str, api_key: str, min_price=None, max_price=None) -> list:
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": api_key,
        "num": 20,
        "gl": "ca",     # Canada
        "hl": "en",
    }
    if min_price: params["tbs"] = f"mr:1,price:1,ppr_min:{min_price}"
    if max_price: params["tbs"] = f"mr:1,price:1,ppr_max:{max_price}"
    if min_price and max_price:
        params["tbs"] = f"mr:1,price:1,ppr_min:{min_price},ppr_max:{max_price}"

    try:
        r = requests.get("https://serpapi.com/search", params=params, timeout=15)
        data = r.json()
        return data.get("shopping_results", [])
    except Exception as e:
        st.error(f"API error: {e}")
        return []


def stars(rating):
    if not rating: return "—"
    full = int(rating)
    half = 1 if (rating - full) >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + "½" * half + "☆" * empty


def render_card(item):
    title = item.get("title", "Unknown Product")
    price_str = item.get("price", "")
    old_price_str = item.get("was_price", "")
    source = item.get("source", "")
    link = item.get("link", "#")
    rating = item.get("rating")
    reviews = item.get("reviews")
    condition = item.get("condition", "New")
    thumbnail = item.get("thumbnail", "")

    # Parse prices
    def parse_price(s):
        if not s: return None
        try: return float(s.replace("$","").replace(",","").replace("CAD","").strip())
        except: return None

    price_val = parse_price(price_str)
    old_val = parse_price(old_price_str)

    discount_pct = ""
    if price_val and old_val and old_val > price_val:
        pct = round((old_val - price_val) / old_val * 100)
        discount_pct = f"-{pct}%"

    price_display = price_str or "—"
    original_display = old_price_str if discount_pct else ""
    discount_tag = f'<span class="card-discount">{discount_pct}</span>' if discount_pct else ""
    original_tag = f'<span class="card-original">{original_display}</span>' if original_display else ""
    rating_display = f'<span class="rating-stars">{stars(rating)}</span> {rating}/5' if rating else "No rating"
    reviews_display = f"({reviews:,} reviews)" if reviews else ""
    condition_display = condition or "New"
    source_display = source.upper() if source else "UNKNOWN"

    st.markdown(f"""
    <div class="product-card">
        <span class="card-source">{source_display}</span>
        <div class="card-title">{title}</div>
        <div>
            <span class="card-price">{price_display}</span>
            {original_tag}
            {discount_tag}
        </div>
        <div class="card-meta">
            <div class="meta-item">
                <span class="meta-label">RATING</span>
                <span class="meta-val">{rating_display} {reviews_display}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">CONDITION</span>
                <span class="meta-val">{condition_display}</span>
            </div>
        </div>
        <a class="card-link" href="{link}" target="_blank">VIEW PRODUCT →</a>
    </div>
    """, unsafe_allow_html=True)


# ── Mode A: Specific model ────────────────────────────────────────────────────
if "Search specific model" in mode:
    st.markdown("")
    query = st.text_input("Model / product name", placeholder="e.g. iPad Air 13-inch M3, Sony WH-1000XM5")

    col1, col2 = st.columns([1, 1])
    with col1:
        min_p = st.number_input("Min price ($CAD)", min_value=0, value=0, step=10)
    with col2:
        max_p = st.number_input("Max price ($CAD)", min_value=0, value=0, step=10,
                                help="Leave 0 for no limit")

    sort_by = st.selectbox("Sort by", ["Price: Low to High", "Price: High to Low", "Best Rating", "Most Reviews"])

    if st.button("SEARCH PRICES"):
        if not api_key:
            st.warning("Add your SerpAPI key in the Setup section above.")
        elif not query:
            st.warning("Enter a product name.")
        else:
            with st.spinner("Scanning the web..."):
                results = fetch_shopping_results(
                    query, api_key,
                    min_price=min_p if min_p > 0 else None,
                    max_price=max_p if max_p > 0 else None
                )

            if not results:
                st.markdown('<div class="no-results">NO RESULTS FOUND — try a broader search term</div>', unsafe_allow_html=True)
            else:
                # Sort
                def sort_key(x):
                    def p(s):
                        try: return float(str(s).replace("$","").replace(",","").strip())
                        except: return 0
                    if sort_by == "Price: Low to High": return p(x.get("price","999999"))
                    if sort_by == "Price: High to Low": return -p(x.get("price","0"))
                    if sort_by == "Best Rating": return -(x.get("rating") or 0)
                    if sort_by == "Most Reviews": return -(x.get("reviews") or 0)
                    return 0

                results = sorted(results, key=sort_key)
                st.markdown(f'<div class="results-header">// {len(results)} RESULTS FOR "{query.upper()}"</div>', unsafe_allow_html=True)
                for item in results:
                    render_card(item)

# ── Mode B: Category + budget ─────────────────────────────────────────────────
else:
    st.markdown("")
    category = st.selectbox(
        "Category",
        ["Headphones", "iPad", "Laptop", "Mechanical Keyboard", "Monitor",
         "Graphics Card", "Earbuds", "Smartphone", "Tablet", "Gaming Chair",
         "Webcam", "Microphone", "SSD", "Custom..."]
    )

    custom_cat = ""
    if category == "Custom...":
        custom_cat = st.text_input("Enter category", placeholder="e.g. gaming mouse, standing desk")

    budget = st.slider("Max budget ($CAD)", min_value=25, max_value=2000, value=200, step=25)

    sort_by2 = st.selectbox("Sort by", ["Price: Low to High", "Best Rating", "Most Reviews", "Price: High to Low"])

    if st.button("FIND DEALS"):
        if not api_key:
            st.warning("Add your SerpAPI key in the Setup section above.")
        else:
            search_term = custom_cat if category == "Custom..." else category
            query = f"best {search_term} under ${budget} CAD"
            with st.spinner(f"Finding the best {search_term} under ${budget}..."):
                results = fetch_shopping_results(query, api_key, max_price=budget)

            if not results:
                st.markdown('<div class="no-results">NO RESULTS — try adjusting budget or category</div>', unsafe_allow_html=True)
            else:
                def sort_key2(x):
                    def p(s):
                        try: return float(str(s).replace("$","").replace(",","").strip())
                        except: return 0
                    if sort_by2 == "Price: Low to High": return p(x.get("price","999999"))
                    if sort_by2 == "Price: High to Low": return -p(x.get("price","0"))
                    if sort_by2 == "Best Rating": return -(x.get("rating") or 0)
                    if sort_by2 == "Most Reviews": return -(x.get("reviews") or 0)
                    return 0

                results = sorted(results, key=sort_key2)
                st.markdown(f'<div class="results-header">// {len(results)} {search_term.upper()} UNDER ${budget} CAD</div>', unsafe_allow_html=True)
                for item in results:
                    render_card(item)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<p style="font-family: 'Space Mono', monospace; font-size: 0.65rem; color: #333; text-align: center; letter-spacing: 1px;">
PRICEPULSE // POWERED BY SERPAPI GOOGLE SHOPPING // 100 FREE SEARCHES/MONTH
</p>
""", unsafe_allow_html=True)
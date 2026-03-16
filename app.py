import streamlit as st
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="مطبخ مريوم", layout="wide")

# 2. تصميم CSS محسن (الخلفية الخشبية وتصغير الصور)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-image: url("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/454fa9d2e598bae3df9c21c1ccf14889.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
        direction: rtl;
    }
    .main-title { color: #f39c12; text-align: center; font-size: 50px; font-weight: 900; text-shadow: 2px 2px 4px #000; }
    .stButton > button {
        width: 100%; height: 70px; font-size: 20px !important;
        background-color: rgba(0,0,0,0.6); color: #f1c40f;
        border: 2px solid #f39c12; border-radius: 15px;
    }
    .recipe-card {
        background-color: rgba(255, 255, 255, 0.95); padding: 15px;
        border-radius: 20px; border-right: 10px solid #f39c12;
        margin-bottom: 20px; color: #333; max-width: 500px; margin-left: auto; margin-right: auto;
    }
    .recipe-img { width: 100%; max-height: 250px; object-fit: cover; border-radius: 15px; }
    .suggestion-text { color: #d35400; font-weight: bold; background: #fff3e0; padding: 5px; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# قائمة البدائل "المناسبة" والمنطقية
alternatives = {
    "لحم": "دجاج أو فطر أو فول صويا", "تمن": "برغل أو فريكة", "سلق": "ورق عنب أو لهانة",
    "طماطم": "معجون طماطم مخفف", "بصل": "كراث أو بصل أخضر", "زيت": "زبدة أو راشي (بالحلو)",
    "هيل": "فانيلا أو قرفة", "ليمون": "خل أو نارنج أو ملح ليمون", "حليب": "زبادي مخفف أو حليب بودرة",
    "طحين": "نشاء أو سميد ناعم", "شكر": "عسل أو دبس تمر", "بيض": "زبادي (بالمعجنات)"
}

if 'page' not in st.session_state: st.session_state.page = 'home'
if 'category' not in st.session_state: st.session_state.category = None

try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
except: recipes = []

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-title">🥘 مطبخ مريوم الذكي</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("🍱 أطباق رئيسية"):
            st.session_state.category, st.session_state.page = "اطباق رئيسية", 'filter'
            st.rerun()
        if st.button("🥗 مقبلات"):
            st.session_state.category, st.session_state.page = "مقبلات", 'filter'
            st.rerun()
    with col2:
        if st.button("🍰 حلويات"):
            st.session_state.category, st.session_state.page = "حلويات", 'filter'
            st.rerun()
        if st.button("🥦 خضروات"):
            st.session_state.category, st.session_state.page = "خضروات", 'filter'
            st.rerun()

# --- صفحة النتائج ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ رجوع"):
        st.session_state.page = 'home'
        st.rerun()
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([i for r in cat_recipes for i in r['ingredients']])))
    user_ing = st.multiselect("شنو عندج مواد؟", all_ing)
    
    if st.button("اكتشفي الأكلات ✨"):
        for res in cat_recipes:
            missing = [m for m in res['ingredients'] if m not in user_ing]
            if len(missing) <= 1:
                st.markdown(f'<div class="recipe-card">', unsafe_allow_html=True)
                st.markdown(f'<h2 style="color:#2c3e50; text-align:center;">{res["name"]}</h2>', unsafe_allow_html=True)
                st.image(res['image'], use_container_width=True)
                st.markdown(f'<p>📖 <b>الطريقة:</b> {res["recipe"]}</p>', unsafe_allow_html=True)
                if len(missing) == 1:
                    alt = alternatives.get(missing[0], "مكون بديل متوفر عندج")
                    st.markdown(f'<p class="suggestion-text">💡 ناقصج {missing[0]}؟ البديل المناسب: {alt}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

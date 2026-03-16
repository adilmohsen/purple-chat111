import streamlit as st
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="مطبخ مريوم", layout="wide")

# 2. تصميم CSS احترافي وشامل للترتيب والخلفية
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;900&display=swap');

    /* تثبيت الخلفية الخشبية على كامل الصفحة */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-image: url("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/454fa9d2e598bae3df9c21c1ccf14889.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        direction: rtl;
    }

    /* العنوان الرئيسي */
    .main-title {
        color: #f39c12;
        text-align: center;
        font-size: clamp(30px, 5vw, 55px);
        font-weight: 900;
        margin-top: 20px;
        text-shadow: 3px 3px 6px #000;
    }

    /* تنسيق الأزرار (2 يمين و 2 يسار) */
    .stButton > button {
        width: 100%;
        height: 80px;
        font-size: 22px !important;
        background-color: rgba(255, 255, 255, 0.1);
        color: #f1c40f;
        border: 2px solid #f39c12;
        border-radius: 20px;
        backdrop-filter: blur(8px);
        margin-bottom: 20px;
        transition: 0.3s;
    }

    .stButton > button:hover {
        background-color: #f39c12;
        color: white;
        transform: scale(1.05);
    }

    /* تنسيق كروت الأكلات وتصغير الصور */
    .recipe-card {
        background-color: rgba(0, 0, 0, 0.8);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #f39c12;
        margin-bottom: 20px;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
        color: white;
    }

    .recipe-img {
        width: 100%;
        max-height: 200px; /* تصغير الصور */
        object-fit: cover;
        border-radius: 15px;
    }

    .suggestion-box {
        background-color: rgba(243, 156, 18, 0.2);
        padding: 10px;
        border-radius: 10px;
        color: #f1c40f;
        font-size: 14px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# قائمة البدائل الشاملة
alternatives = {
    "لحم": "دجاج أو بزاليا", "تمن": "برغل", "سلق": "ورق عنب", "طماطم": "معجون",
    "بصل": "كراث", "زيت": "زبدة", "هيل": "دارسين", "ليمون": "خل",
    "طحين": "نشاء", "حليب": "زبادي مخفف", "تمر": "عسل", "سمك": "دجاج"
}

if 'page' not in st.session_state: st.session_state.page = 'home'
if 'category' not in st.session_state: st.session_state.category = None

# تحميل البيانات
try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
except: recipes = []

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-title">🥘 مطبخ مريوم الذكي</div>', unsafe_allow_html=True)
    
    # توزيع الأزرار 2 يمين و 2 يسار باستخدام أعمدة متوازنة
    st.write("###") # مساحة علوية
    col1, spacer, col2 = st.columns([2, 1, 2])
    
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

# --- صفحة التصفية ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ رجوع"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.markdown(f"<h2 style='text-align:center; color:white;'>شنو عندج للـ {st.session_state.category}؟</h2>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([i for r in cat_recipes for i in r['ingredients']])))
    user_ing = st.multiselect("اختاري المواد المتوفرة:", all_ing)
    
    if st.button("اكتشفي الأكلات ✨"):
        for res in cat_recipes:
            missing = [m for m in res['ingredients'] if m not in user_ing]
            if len(missing) <= 1:
                st.markdown(f'''
                <div class="recipe-card">
                    <h2 style="color:#f1c40f; text-align:center;">{res['name']}</h2>
                    <img src="{res['image']}" class="recipe-img">
                    <p style="margin-top:10px;"><b>💰 التكلفة:</b> {res['cost']}</p>
                    <p><b>📖 الطريقة:</b> {res['recipe']}</p>
                ''', unsafe_allow_html=True)
                if len(missing) == 1:
                    alt = alternatives.get(missing[0], "مكون آخر من المطبخ")
                    st.markdown(f'<div class="suggestion-box">💡 ناقصج {missing[0]}؟ بديله: {alt}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

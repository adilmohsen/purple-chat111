import streamlit as st
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="مطبخ مريوم", layout="wide")

# 2. تصميم CSS احترافي يحل كل مشاكل الترتيب
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;900&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-image: url("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/454fa9d2e598bae3df9c21c1ccf14889.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        direction: rtl;
    }

    .main-title {
        color: #f39c12;
        text-align: center;
        font-size: 55px;
        font-weight: 900;
        margin-top: 20px;
        text-shadow: 3px 3px 6px #000;
    }

    /* تنسيق توزيع الأزرار 2 يمين و 2 يسار */
    .button-container {
        display: flex;
        justify-content: space-between;
        padding: 50px 100px;
    }

    .stButton > button {
        width: 250px;
        height: 80px;
        font-size: 22px !important;
        font-weight: bold;
        background-color: rgba(255, 255, 255, 0.15);
        color: #f1c40f;
        border: 2px solid #f39c12;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.5);
    }

    .stButton > button:hover {
        background-color: #f39c12;
        color: white;
        transform: scale(1.05);
    }

    /* تصغير كروت الأكلات وصورها */
    .recipe-card {
        background-color: rgba(0, 0, 0, 0.85);
        padding: 15px;
        border-radius: 20px;
        border: 2px solid #f39c12;
        margin-bottom: 20px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    .recipe-img {
        width: 100%;
        max-height: 250px;
        object-fit: cover;
        border-radius: 15px;
    }

    .suggestion-box {
        background-color: rgba(243, 156, 18, 0.2);
        padding: 10px;
        border-radius: 10px;
        font-size: 14px;
        color: #f1c40f;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# البدائل الشاملة (شكو شي بالمطبخ)
alternatives = {
    "لحم": "دجاج أو بزاليا", "تمن": "برغل", "سلق": "ورق عنب", "طماطم": "معجون طماطم",
    "بصل": "كراث", "زيت": "زبدة أو دهن", "هيل": "دارسين", "ليمون": "خل أو ملح ليمون",
    "خبز": "صمون", "طحين": "نشاء", "حليب": "زبادي مخفف", "تمر": "عسل أو دبس"
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
    
    # توزيع الأزرار يدوياً لضمان الشكل (2 يمين، 2 يسار)
    col_left, col_mid, col_right = st.columns([2, 1, 2])
    
    with col_left:
        st.write("") # فراغ
        if st.button("🍱 أطباق رئيسية"):
            st.session_state.category, st.session_state.page = "اطباق رئيسية", 'filter'
            st.rerun()
        st.write("")
        if st.button("🥗 مقبلات"):
            st.session_state.category, st.session_state.page = "مقبلات", 'filter'
            st.rerun()
            
    with col_right:
        st.write("")
        if st.button("🍰 حلويات"):
            st.session_state.category, st.session_state.page = "حلويات", 'filter'
            st.rerun()
        st.write("")
        if st.button("🥦 خضروات"):
            st.session_state.category, st.session_state.page = "خضروات", 'filter'
            st.rerun()

# --- صفحة الاقتراحات ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ رجوع"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.markdown(f"<h2 style='text-align:center; color:#f39c12;'>شنو عندج للـ {st.session_state.category}؟</h2>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([i for r in cat_recipes for i in r['ingredients']])))
    user_ing = st.multiselect("اختاري المواد المتوفرة:", all_ing)
    
    if st.button("اكتشفي الأكلات ✨"):
        for res in cat_recipes:
            missing = [m for m in res['ingredients'] if m not in user_ing]
            if len(missing) <= 1:
                st.markdown(f'''
                <div class="recipe-card">
                    <h2 style="color:#f1c40f;">{res['name']}</h2>
                    <img src="{res['image']}" class="recipe-img">
                    <p style="color:white; margin-top:10px;"><b>الطريقة:</b> {res['recipe']}</p>
                ''', unsafe_allow_html=True)
                if len(missing) == 1:
                    alt = alternatives.get(missing[0], "مكون بديل من عندج")
                    st.markdown(f'<div class="suggestion-box">💡 ناقصج {missing[0]}؟ بديله: {alt}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

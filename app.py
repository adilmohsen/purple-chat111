import streamlit as st
import json

# 1. إعداد الصفحة وتثبيتها بالمنتصف
st.set_page_config(page_title="مطبخ مريوم", layout="centered")

# 2. CSS: قفل الإعدادات (الخط، الألوان، حجم الصورة، الأزرار)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-color: #fff1f2; /* ثيم وردي هادئ ثابت */
        direction: rtl;
    }

    .main-title { 
        color: #db2777; text-align: center; font-size: 50px; font-weight: 900; 
        margin-top: 20px; margin-bottom: 30px;
    }

    /* الأزرار: منتصف الشاشة، لا ميلان لليمين ولا لليسار */
    .stButton > button {
        width: 100%; height: 75px; font-size: 22px !important;
        background-color: #ffffff; color: #be185d;
        border: 2px solid #fbcfe8; border-radius: 20px;
        font-weight: 900; margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stButton > button:hover {
        background-color: #f472b6; color: white;
    }

    /* كرت الأكلة وحجم الصورة (ثابت وصغير) */
    .recipe-card {
        background: white; padding: 20px; border-radius: 25px;
        margin-top: 20px; text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    
    .stImage img {
        border-radius: 15px;
        width: 300px !important; /* حجم صغير جداً ونازك */
        margin: 0 auto;
    }

    .advice-text {
        color: #9f1239; font-size: 18px; font-weight: bold;
        background: #ffe4e6; padding: 15px; border-radius: 15px;
        margin: 15px 0; border-right: 5px solid #fb7185;
    }
</style>
""", unsafe_allow_html=True)

# النصائح والبدائل (ثابتة)
smart_tips = {
    "خيار": "ما عندج خيار؟ استعملي لهانة مفرومة ناعم أو مخلل، تنطيج نفس القرمشة والحموضة 🥗",
    "لحم": "الفطر المتبل بالبهارات بديل ممتاز يخلي الأكلة خفيفة وصحية 🍄",
    "تمن": "البديل هو البرغل، يشبع وينطي نكهة تراثية تجنن 🌾",
    "طماطم": "المعجون ويه رشة شكر صغيرة يعوض طعم الطماطم الفريش 🍅"
}

if 'page' not in st.session_state: st.session_state.page = 'home'
if 'category' not in st.session_state: st.session_state.category = None

try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
except: recipes = []

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-title">🎀 مطبخ مريوم 🎀</div>', unsafe_allow_html=True)
    
    # وضع الأزرار في عمود واحد مركزي لضمان التناسق التام
    _, center_col, _ = st.columns([0.5, 2, 0.5])
    with center_col:
        if st.button("🍱 أطباق رئيسية"):
            st.session_state.category, st.session_state.page = "اطباق رئيسية", 'filter'
            st.rerun()
        if st.button("🥗 مقبلات"):
            st.session_state.category, st.session_state.page = "مقبلات", 'filter'
            st.rerun()
        if st.button("🍰 حلويات"):
            st.session_state.category, st.session_state.page = "حلويات", 'filter'
            st.rerun()
        if st.button("🥦 خضروات"):
            st.session_state.category, st.session_state.page = "خضروات", 'filter'
            st.rerun()

# --- صفحة الفلترة والنتائج ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ رجوع"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"<h2 style='text-align:center; color:#be185d;'>شنو متوفر بمطبخج؟</h2>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([i for r in cat_recipes for i in r['ingredients']])))
    user_ing = st.multiselect("المواد المتوفرة:", all_ing)
    
    if st.button("اكتشفي الأكلات ✨"):
        for res in cat_recipes:
            missing = [m for m in res['ingredients'] if m not in user_ing]
            if len(missing) <= 1:
                st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                st.markdown(f'<h2 style="color:#db2777;">{res["name"]}</h2>', unsafe_allow_html=True)
                
                # الصورة صغيرة وبالمنتصف
                st.image(res['image'])
                
                if len(missing) == 1:
                    tip = smart_tips.get(missing[0], "استخدمي أي بديل متوفر من المطبخ!")
                    st.markdown(f'<div class="advice-text">💡 نصيحة مريوم: {tip}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div style="text-align:right;"><b>👩‍🍳 الطريقة:</b><br>{res["recipe"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

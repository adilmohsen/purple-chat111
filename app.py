import streamlit as st
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="مطبخ مريوم", layout="centered")

# 2. CSS: تثبيت الخط العريض وتوسيط الأزرار وتصغير الصورة
st.markdown("""
<style>
    /* استدعاء خط Cairo العريض */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-color: #fff1f2; 
        direction: rtl;
    }

    /* عنوان كبير وواضح */
    .main-title { 
        color: #db2777; text-align: center; font-size: 55px; 
        font-weight: 900; margin-bottom: 40px;
    }

    /* الأزرار: كبيرة، واضحة، وفي منتصف الشاشة تماماً */
    .stButton > button {
        width: 100%; height: 85px; font-size: 26px !important;
        background-color: #ffffff; color: #be185d;
        border: 3px solid #fbcfe8; border-radius: 25px;
        font-weight: 900; margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .stButton > button:hover {
        background-color: #f472b6; color: white;
    }

    /* حجم الصورة: صغير ومرتب بوسط الكرت */
    .stImage img {
        border-radius: 20px;
        width: 320px !important; 
        margin: 0 auto;
        display: block;
    }

    .recipe-card {
        background: white; padding: 25px; border-radius: 30px;
        text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'home'

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-title">🎀 مطبخ مريوم 🎀</div>', unsafe_allow_html=True)
    
    # حصر الأزرار في عمود واحد مركزي لضمان عدم ميلانها
    _, center_col, _ = st.columns([0.4, 2, 0.4])
    with center_col:
        if st.button("🍱 أطباق رئيسية"):
            st.session_state.page = 'filter'
            st.rerun()
        if st.button("🥗 مقبلات"):
            st.session_state.page = 'filter'
            st.rerun()
        if st.button("🍰 حلويات"):
            st.session_state.page = 'filter'
            st.rerun()
        if st.button("🥦 خضروات"):
            st.session_state.page = 'filter'
            st.rerun()

# --- صفحة النتائج ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ رجوع"):
        st.session_state.page = 'home'
        st.rerun()
    
    # مثال لعرض الصورة بحجمها الصغير الجديد
    st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#db2777; font-weight:900;">كليجة تمر</h2>', unsafe_allow_html=True)
    st.image("https://via.placeholder.com/300") # مكان الصورة
    st.markdown('<p style="font-weight:900; font-size:20px;">الطريقة: عجينة محشوة بالتمر والهيل وتُشوى بالفرن.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

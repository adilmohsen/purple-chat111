import streamlit as st
import json

# 1. إعداد الصفحة بشكل كامل
st.set_page_config(page_title="مطبخ مريوم", layout="wide")

# 2. تصميم CSS (خط Cairo، ألوان سمائي ووردي، خلفية ثابتة)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-color: #f0f8ff; /* لون سمائي فاتح جداً للخلفية */
        direction: rtl;
    }

    /* العنوان الرئيسي بتصميم وردي وذهبي */
    .main-title { 
        color: #ff69b4; text-align: center; font-size: 65px; font-weight: 900; 
        text-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-top: 30px;
    }

    /* تنسيق الأزرار (سمائي مع حواف وردية) */
    .stButton > button {
        width: 100%; height: 85px; font-size: 24px !important;
        background-color: #87ceeb; color: white;
        border: 3px solid #ffb6c1; border-radius: 20px;
        transition: 0.3s; font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #ffb6c1; color: white; transform: scale(1.02);
    }

    /* كروت النتائج (تصميم نظيف بلمسة وردية) */
    .recipe-card {
        background-color: white; padding: 35px;
        border-radius: 25px; border-right: 15px solid #ff69b4;
        margin-bottom: 35px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    .recipe-title { color: #4682b4; font-size: 40px; font-weight: 900; text-align: center; }
    
    /* شريط البدائل */
    .suggestion-box {
        background: #e0f7fa; border-right: 8px solid #00acc1;
        padding: 15px; border-radius: 12px; color: #00838f;
        font-weight: bold; font-size: 20px; margin-top: 20px;
    }

    /* تكبير الصور لتكون واضحة جداً */
    .stImage img {
        border-radius: 20px; width: 100% !important; max-height: 550px !important; object-fit: cover;
    }
</style>
""", unsafe_allow_html=True)

# قائمة البدائل الذكية (خيار، لحم، تمن، إلخ)
smart_alts = {
    "خيار": "مخلل أو لهانة مفرومة", "لحم": "دجاج أو فطر متبل", "تمن": "برغل",
    "طماطم": "معجون مخفف", "بصل": "بصل أخضر", "زيت": "زبدة",
    "هيل": "دارسين", "ليمون": "نارنج أو خل", "حليب": "زبادي"
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
    
    # توزيع الأزرار بالنص (2 يمين و 2 يسار)
    col_r, spacer, col_l = st.columns([2, 0.4, 2])
    with col_r:
        if st.button("🍱 أطباق رئيسية"):
            st.session_state.category, st.session_state.page = "اطباق رئيسية", 'filter'
            st.rerun()
        if st.button("🥗 مقبلات"):
            st.session_state.category, st.session_state.page = "مقبلات", 'filter'
            st.rerun()
    with col_l:
        if st.button("🍰 حلويات"):
            st.session_state.category, st.session_state.page = "حلويات", 'filter'
            st.rerun()
        if st.button("🥦 خضروات"):
            st.session_state.category, st.session_state.page = "خضروات", 'filter'
            st.rerun()

# --- صفحة الفلترة والنتائج ---
elif st.session_state.page == 'filter':
    if st.button("⬅️"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"<h1 style='text-align:center; color:#4682b4; font-size:45px;'>شنو متوفر عندج؟</h1>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([i for r in cat_recipes for i in r['ingredients']])))
    user_ing = st.multiselect("اختاري المواد:", all_ing)
    
    if st.button("اكتشفي الأكلات ✨"):
        found = False
        for res in cat_recipes:
            missing = [m for m in res['ingredients'] if m not in user_ing]
            if len(missing) <= 1:
                found = True
                st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="recipe-title">{res["name"]}</div>', unsafe_allow_html=True)
                
                # عرض الصورة بشكل ضخم وواضح
                st.image(res['image'], use_container_width=True)
                
                if len(missing) == 1:
                    alt_fix = smart_alts.get(missing[0], "مكون بديل")
                    st.markdown(f'<div class="suggestion-box">💡 ناقصج {missing[0]}؟ البديل: {alt_fix}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div style="font-size:24px; color:#333; margin-top:15px;"><b>📖 الطريقة:</b><br>{res["recipe"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        if not found:
            st.warning("اختاري مواد أكثر حتى تطلعلج أكلات!")

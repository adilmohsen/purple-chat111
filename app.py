import streamlit as st
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="مطبخ مريوم", layout="wide")

# 2. تصميم CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-color: #fdfaf5;
        direction: rtl;
    }
    .main-title { color: #5d4037; text-align: center; font-size: 45px; font-weight: 800; margin-bottom: 30px; }
    .stButton > button {
        width: 100%; height: 70px; font-size: 22px !important;
        background-color: #ffffff; color: #5d4037;
        border: 2px solid #d7ccc8; border-radius: 15px;
    }
    .recipe-card {
        background-color: white; padding: 25px; border-radius: 20px;
        border-right: 8px solid #8d6e63; box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        margin-bottom: 25px; text-align: right;
    }
    .suggestion { color: #e67e22; font-weight: bold; font-size: 16px; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# قائمة البدائل الذكية
alternatives = {
    "لحم": "دجاج أو فطر",
    "دهن": "زيت نباتي أو زبدة",
    "سلق": "ورق عنب",
    "تمن": "برغل",
    "ليمون": "مندوزي (ملح الليمون) أو خل",
    "خيار": "شجر (كوسا) مقطع ناعم (للطبخ)",
    "دبس رمان": "تمر هندي أو عصير ليمون مع شكر"
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
    st.image("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/image_bbb3fd.png", use_container_width=True)
    st.markdown('<div class="main-title">🍴 مطبخ مريوم الحلوة</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        if st.button("🥘 أطباق رئيسية"):
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

# --- صفحة الفلترة والبدائل ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ رجوع"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.markdown(f"<h2 style='text-align:right;'>شنو عندج مواد للـ {st.session_state.category}؟</h2>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([ing for r in cat_recipes for ing in r['ingredients']])))
    user_ing = st.multiselect("اختاري المواد المتوفرة:", all_ing)
    
    if st.button("اكتشفي الأكلات ✨"):
        if user_ing:
            for res in cat_recipes:
                missing = [m for m in res['ingredients'] if m not in user_ing]
                
                # إذا كانت كل المواد موجودة أو ناقص مادة وحدة بس
                if len(missing) <= 1:
                    st.markdown(f'<div class="recipe-card">', unsafe_allow_html=True)
                    st.markdown(f'<h2 style="color:#5d4037;">{res["name"]}</h2>', unsafe_allow_html=True)
                    
                    if len(missing) == 1:
                        m_item = missing[0]
                        alt_text = alternatives.get(m_item, "مادة ثانية متوفرة عندج")
                        st.markdown(f'<p class="suggestion">💡 ناقصج {m_item}؟ ممكن تستخدمين {alt_text} بداله.</p>', unsafe_allow_html=True)
                    
                    st.markdown(f'<p>💰 <b>التكلفة:</b> {res["cost"]}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p>📖 <b>الطريقة:</b> {res["recipe"]}</p>', unsafe_allow_html=True)
                    st.image(res['image'], use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("مريوم، اختاري مادة على الأقل.")

import streamlit as st
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="مطبخ مريوم", layout="wide")

# 2. تصميم CSS (خط جبير، أيقونات، صور ضخمة)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-image: url("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/454fa9d2e598bae3df9c21c1ccf14889.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
        direction: rtl;
    }

    /* تكبير الخط لكل الموقع */
    h1, h2, h3, p, span, button {
        font-family: 'Cairo', sans-serif !important;
    }

    .main-title { 
        color: #f1c40f; text-align: center; font-size: 70px; font-weight: 900; 
        text-shadow: 4px 4px 10px #000; margin-bottom: 20px;
    }

    /* زر الرجوع (أيقونة فقط) */
    .back-btn button {
        width: 60px !important; height: 60px !important; font-size: 30px !important;
        border-radius: 50% !important; background: rgba(0,0,0,0.5) !important;
    }

    /* كروت الأكلات والصور الضخمة */
    .recipe-card {
        background-color: rgba(255, 255, 255, 0.98); padding: 40px;
        border-radius: 30px; border-top: 20px solid #f39c12;
        margin-bottom: 40px; color: #2c3e50; box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    
    .recipe-title { color: #d35400; font-size: 45px; font-weight: 900; text-align: center; margin-bottom: 20px; }
    
    .recipe-text { font-size: 24px; line-height: 1.6; }

    .suggestion-box {
        background: #fff3e0; border-right: 8px solid #e67e22;
        padding: 20px; border-radius: 15px; color: #d35400;
        font-weight: bold; font-size: 22px; margin: 20px 0;
    }

    /* تكبير الصورة لتكون واضحة جداً */
    .stImage img {
        border-radius: 25px; width: 100% !important; max-height: 600px !important; object-fit: cover;
    }
</style>
""", unsafe_allow_html=True)

# قائمة البدائل (شكو شي بالمطبخ)
alternatives = {
    "لحم": "دجاج أو فطر", "تمن": "برغل", "سلق": "ورق عنب", "طماطم": "معجون",
    "بصل": "كراث", "زيت": "زبدة", "هيل": "دارسين", "ليمون": "خل",
    "طحين": "نشاء", "حليب": "زبادي مخفف", "تمر": "عسل", "دهن": "زيت أو زبدة"
}

if 'page' not in st.session_state: st.session_state.page = 'home'
if 'category' not in st.session_state: st.session_state.category = None

try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
except: recipes = []

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-title">🍴 مطبخ مريوم</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
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

# --- صفحة الفلترة والنتائج ---
elif st.session_state.page == 'filter':
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️"):
        st.session_state.page = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f"<h1 style='text-align:center; color:white; font-size:50px;'>شنو عندج للـ {st.session_state.category}؟</h1>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([i for r in cat_recipes for i in r['ingredients']])))
    user_ing = st.multiselect("اختاري المواد المتوفرة:", all_ing)
    
    if st.button("اكتشفي الأكلات ✨"):
        found = False
        for res in cat_recipes:
            missing = [m for m in res['ingredients'] if m not in user_ing]
            if len(missing) <= 1:
                found = True
                st.markdown(f'<div class="recipe-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="recipe-title">{res["name"]}</div>', unsafe_allow_html=True)
                
                # عرض الصورة بحجم كبير جداً
                st.image(res['image'], use_container_width=True)
                
                if len(missing) == 1:
                    alt = alternatives.get(missing[0], "مكون بديل")
                    st.markdown(f'<div class="suggestion-box">💡 ناقصج {missing[0]}؟ البديل: {alt}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="recipe-text"><b>📖 الطريقة:</b><br>{res["recipe"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        if not found:
            st.warning("مريوم، اختاري مواد أكثر حتى تطلعلج الأكلات!")

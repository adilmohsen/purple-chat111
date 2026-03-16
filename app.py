import streamlit as st
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="مطبخ مريوم الذكي", layout="wide")

# 2. تصميم CSS احترافي (الخلفية، الأزرار، الخطوط)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-image: url("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/454fa9d2e598bae3df9c21c1ccf14889.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
        direction: rtl;
    }

    .main-title { 
        color: #f1c40f; text-align: center; font-size: 60px; font-weight: 900; 
        text-shadow: 3px 3px 10px #000; margin-bottom: 40px;
    }

    /* توزيع الأزرار في المنتصف */
    .stButton > button {
        width: 100%; height: 90px; font-size: 26px !important;
        background-color: rgba(0,0,0,0.7); color: #f1c40f;
        border: 3px solid #f39c12; border-radius: 25px;
        transition: 0.4s; font-weight: 900;
    }
    .stButton > button:hover {
        background-color: #f39c12; color: white; transform: scale(1.05);
    }

    /* كروت الأكلات والصور الكبيرة */
    .recipe-card {
        background-color: rgba(255, 255, 255, 0.98); padding: 30px;
        border-radius: 30px; border-top: 15px solid #d35400;
        margin-bottom: 40px; color: #2c3e50; box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    .recipe-title { color: #d35400; font-size: 40px; font-weight: 900; text-align: center; }
    
    /* شريط البدائل الذكي */
    .suggestion-box {
        background: #fff3e0; border-right: 10px solid #e67e22;
        padding: 20px; border-radius: 15px; color: #d35400;
        font-weight: bold; font-size: 22px; margin: 25px 0;
    }
</style>
""", unsafe_allow_html=True)

# قائمة البدائل "الذكية" للمطبخ العراقي
smart_alts = {
    "خيار": "مخلل أو لهانة مفرومة", "لحم": "دجاج أو فطر متبل", "تمن": "برغل ناعم",
    "طماطم": "معجون مخفف بليمون", "بصل": "كراث أو بصل أخضر", "زيت": "زبدة أو راشي",
    "هيل": "فانيلا أو دارسين", "ليمون": "نارنج أو ملح ليمون", "حليب": "زبادي مخفف",
    "طحين": "نشاء أو سميد", "شكر": "دبس أو عسل", "بيض": "ملعقة زبادي كبيرة",
    "بقدونس": "كزبرة خضراء", "بطاطا": "جزر مسلوق", "فلفل": "شطة حارة"
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
    
    col_r, spacer, col_l = st.columns([2, 0.5, 2])
    with col_r:
        if st.button("🥘 أطباق رئيسية"):
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

# --- صفحة النتائج ---
elif st.session_state.page == 'filter':
    if st.button("⬅️"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"<h1 style='text-align:center; color:white; font-size:45px;'>شنو عندج للـ {st.session_state.category}؟</h1>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([i for r in cat_recipes for i in r['ingredients']])))
    user_ing = st.multiselect("اختاري المواد المتوفرة:", all_ing)
    
    if st.button("اكتشفي الأكلات ✨"):
        for res in cat_recipes:
            missing = [m for m in res['ingredients'] if m not in user_ing]
            # تظهر الأكلة إذا كانت كاملة أو ناقصها مادة واحدة فقط
            if len(missing) <= 1:
                st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="recipe-title">{res["name"]}</div>', unsafe_allow_html=True)
                
                # عرض الصورة بشكل كبير
                st.image(res['image'], use_container_width=True)
                
                if len(missing) == 1:
                    alt_fix = smart_alts.get(missing[0], "مكون آخر متوفر")
                    st.markdown(f'<div class="suggestion-box">💡 ناقصج {missing[0]}؟ البديل المناسب هو: {alt_fix}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div style="font-size:22px;"><b>📖 الطريقة:</b><br>{res["recipe"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

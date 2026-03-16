import streamlit as st
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="مطبخ مريوم", layout="wide")

# 2. CSS المتطور: ألوان متناسقة، خط Cairo، وترتيب أزرار احترافي
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-color: #fdf2f8; /* خلفية وردية هادئة جداً */
        direction: rtl;
    }

    .main-title { 
        color: #db2777; text-align: center; font-size: 55px; font-weight: 900; 
        margin-top: 20px; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    /* تنسيق الأزرار بشكل متناسق في منتصف الشاشة */
    .stButton > button {
        width: 100%; height: 100px; font-size: 24px !important;
        background-color: #ffffff; color: #be185d;
        border: 2px solid #fbcfe8; border-radius: 30px;
        box-shadow: 0 4px 15px rgba(219, 39, 119, 0.1);
        transition: 0.3s all ease; font-weight: 900;
    }
    .stButton > button:hover {
        background-color: #f472b6; color: white; transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(219, 39, 119, 0.2);
    }

    /* كرت النصائح الذكي */
    .advice-box {
        background: #fff1f2; border-right: 10px solid #fb7185;
        padding: 20px; border-radius: 20px; color: #9f1239;
        font-size: 20px; line-height: 1.6; margin: 20px 0;
    }

    /* كرت الأكلة */
    .recipe-card {
        background: white; padding: 25px; border-radius: 35px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.05); margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# نظام النصائح والبدائل الذكي (بديل + نصيحة للطعم)
smart_tips = {
    "خيار": "ما عندج خيار؟ استعملي لهانة مفرومة ناعم أو مخلل، راح تنطيج نفس القرمشة والحموضة المطلوبة 🥗",
    "لحم": "إذا اللحم ما متوفر، الفطر المتبل بالبهارات ينطي طعم قريب ويخلي الأكلة خفيفة وصحية 🍄",
    "تمن": "البديل الأمثل هو البرغل، يشبع أكثر وينطي نكهة تراثية تجنن للأكلة 🌾",
    "طماطم": "المعجون ويه رشة شكر صغيرة يعوض طعم الطماطم الفريش ويعدل الحموضة 🍅",
    "بصل": "الكراث أو الثوم المهروس ينطون نفس النكهة القوية، بس قللي الكمية شوية 🧅",
    "زيت": "الزبدة راح تنطي دسامة وطعم أطيب بهواية من الزيت العادي 🧈",
    "ليمون": "النارنج أو ملح الليمون (المندوزي) ينطي حموضة أقوى، ديري بالج لا تكثرين 🍋"
}

if 'page' not in st.session_state: st.session_state.page = 'home'
if 'category' not in st.session_state: st.session_state.category = None

try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
except: recipes = []

# --- الصفحة الرئيسية بتوزيع متناسق ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-title">🎀 مطبخ مريوم 🎀</div>', unsafe_allow_html=True)
    
    # توزيع الأزرار بشكل 2x2 متقارب في المنتصف
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
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

# --- صفحة النتائج مع النصائح ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ الرجوع"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"<h2 style='text-align:center; color:#be185d;'>شنو متوفر بمطبخج للـ {st.session_state.category}؟</h2>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([i for r in cat_recipes for i in r['ingredients']])))
    user_ing = st.multiselect("اختاري المكونات اللي عندج:", all_ing)
    
    if st.button("اكتشفي الأكلات ✨"):
        for res in cat_recipes:
            missing = [m for m in res['ingredients'] if m not in user_ing]
            if len(missing) <= 1:
                st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                st.markdown(f'<h1 style="color:#db2777; text-align:center;">{res["name"]}</h1>', unsafe_allow_html=True)
                st.image(res['image'], use_container_width=True)
                
                if len(missing) == 1:
                    tip = smart_tips.get(missing[0], f"ناقصج {missing[0]}؟ لا تهتمين، تكدرين تستبدليه بأي شي قريب عليه من المطبخ ويبقى الطعم طيب!")
                    st.markdown(f'<div class="advice-box">💡 <b>نصيحة مريوم:</b><br>{tip}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div style="font-size:20px;"><b>👩‍🍳 طريقة التحضير:</b><br>{res["recipe"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

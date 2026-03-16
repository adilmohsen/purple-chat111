import streamlit as st
import json

# 1. إعداد الصفحة (ثابتة)
st.set_page_config(page_title="مطبخ مريوم", layout="wide")

# 2. CSS: الألوان والخطوط والأزرار (حسب طلبج الأخير)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-color: #fdf2f8; 
        direction: rtl;
    }

    .main-title { 
        color: #db2777; text-align: center; font-size: 55px; font-weight: 900; 
        margin-top: 20px;
    }

    /* الأزرار: ترتيب رباعي متناسق في المنتصف */
    .stButton > button {
        width: 100%; height: 90px; font-size: 24px !important;
        background-color: #ffffff; color: #be185d;
        border: 2px solid #fbcfe8; border-radius: 25px;
        font-weight: 900;
    }
    .stButton > button:hover {
        background-color: #f472b6; color: white;
    }

    /* كرت الأكلة وحجم الصورة الثابت */
    .recipe-card {
        background: white; padding: 20px; border-radius: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin-bottom: 30px;
    }
    
    /* ضمان ظهور الصورة بشكل صحيح وكبير */
    .stImage > img {
        border-radius: 20px;
        width: 100% !important;
        object-fit: contain !important; /* يحافظ على أبعاد الصورة الأصلية بدون قص */
    }

    .advice-box {
        background: #fff1f2; border-right: 8px solid #fb7185;
        padding: 15px; border-radius: 15px; color: #9f1239;
        font-size: 19px; margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# نظام النصائح والبدائل (ثابت ومحفوظ)
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

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-title">🎀 مطبخ مريوم 🎀</div>', unsafe_allow_html=True)
    
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

# --- صفحة الفلترة والنتائج ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ الرجوع"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"<h2 style='text-align:center; color:#be185d;'>شنو متوفر بمطبخج للـ {st.session_state.category}؟</h2>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([i for r in cat_recipes for i in r['ingredients']])))
    user_ing = st.multiselect("اختاري المكونات:", all_ing)
    
    if st.button("اكتشفي الأكلات ✨"):
        for res in cat_recipes:
            missing = [m for m in res['ingredients'] if m not in user_ing]
            if len(missing) <= 1:
                st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                st.markdown(f'<h1 style="color:#db2777; text-align:center;">{res["name"]}</h1>', unsafe_allow_html=True)
                
                # عرض الصورة (هسة راح تظهر أكيد لأن ثبتنا الكود الخاص بيها)
                st.image(res['image'], use_container_width=True)
                
                if len(missing) == 1:
                    tip = smart_tips.get(missing[0], f"ناقصج {missing[0]}؟ تكدرين تستخدمين أي بديل متوفر وتطلع الأكلة تخبل!")
                    st.markdown(f'<div class="advice-box">💡 <b>نصيحة مريوم:</b><br>{tip}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div style="font-size:20px;"><b>👩‍🍳 الطريقة:</b><br>{res["recipe"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

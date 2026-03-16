import streamlit as st
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="مطبخ مريوم", layout="centered") # التغيير لـ centered لضمان التناسق

# 2. CSS: تنسيق الأزرار وحجم الصورة الصغير
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-color: #fdf2f8; 
        direction: rtl;
    }

    .main-title { 
        color: #db2777; text-align: center; font-size: 50px; font-weight: 900; 
        margin-bottom: 40px;
    }

    /* أزرار متناسقة تماماً في منتصف الصفحة */
    .stButton > button {
        width: 100%; height: 75px; font-size: 22px !important;
        background-color: #ffffff; color: #be185d;
        border: 2px solid #fbcfe8; border-radius: 20px;
        font-weight: 900; margin-bottom: 10px;
    }
    .stButton > button:hover {
        background-color: #f472b6; color: white;
    }

    /* تحديد حجم الصورة ليكون صغيراً ونازكاً */
    .stImage > img {
        border-radius: 15px;
        width: 350px !important; /* حجم صغير ثابت حسب طلبج */
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    .recipe-card {
        background: white; padding: 20px; border-radius: 25px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-top: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# نظام النصائح والبدائل
smart_tips = {
    "خيار": "ما عندج خيار؟ استعملي لهانة مفرومة ناعم أو مخلل، راح تنطيج نفس القرمشة والحموضة المطلوبة 🥗",
    "لحم": "إذا اللحم ما متوفر، الفطر المتبل بالبهارات ينطي طعم قريب ويخلي الأكلة خفيفة وصحية 🍄",
    "تمن": "البديل الأمثل هو البرغل، يشبع أكثر وينطي نكهة تراثية تجنن للأكلة 🌾",
    "طماطم": "المعجون ويه رشة شكر صغيرة يعوض طعم الطماطم الفريش ويعدل الحموضة 🍅"
}

if 'page' not in st.session_state: st.session_state.page = 'home'
if 'category' not in st.session_state: st.session_state.category = None

try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
except: recipes = []

# --- الصفحة الرئيسية: ترتيب الأزرار بمنتصف الشاشة ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-title">🎀 مطبخ مريوم 🎀</div>', unsafe_allow_html=True)
    
    # استخدام عمود واحد في المنتصف لضمان عدم ميلان الأزرار
    _, center_col, _ = st.columns([1, 2, 1])
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

# --- صفحة النتائج ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ رجوع"):
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
                st.markdown(f'<h2 style="color:#db2777;">{res["name"]}</h2>', unsafe_allow_html=True)
                
                # الصورة هسة حجمها صغير وبالنص
                st.image(res['image'])
                
                if len(missing) == 1:
                    tip = smart_tips.get(missing[0], f"ناقصج {missing[0]}؟ تكدرين تستخدمين بديل وتطلع تجنن!")
                    st.markdown(f'<div style="color:#9f1239; margin-top:10px;"><b>💡 نصيحة مريوم:</b><br>{tip}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div style="text-align:right; margin-top:15px;"><b>👩‍🍳 الطريقة:</b><br>{res["recipe"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

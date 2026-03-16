import streamlit as st
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="مطبخ مريوم", page_icon="🍲", layout="centered")

# 2. تصميم CSS لجعل الصورة خلفية كاملة والأزرار مستطيلة فخمة
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/454fa9d2e598bae3df9c21c1ccf14889.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* تنسيق الأزرار المستطيلة الكبيرة */
div.stButton > button {{
    width: 100%;
    height: 80px;
    font-size: 24px !important;
    font-weight: bold;
    border-radius: 12px;
    background-color: rgba(0, 0, 0, 0.5); /* تعتيم خلف الزر لبروزه */
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(8px);
    margin-bottom: 20px;
}}

div.stButton > button:hover {{
    background-color: rgba(255, 255, 255, 0.2);
    border-color: white;
}}

.recipe-card {{
    background-color: rgba(0, 0, 0, 0.7);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: right;
    direction: rtl;
    border: 1px solid rgba(255, 255, 255, 0.2);
}}
</style>
""", unsafe_allow_html=True)

# 3. إدارة التنقل (Navigation)
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'category' not in st.session_state:
    st.session_state.category = None

# تحميل البيانات
try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
except:
    recipes = []

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown("<h1 style='text-align:center; color:white; text-shadow: 2px 2px 4px #000;'>👨‍🍳 مطبخ مريوم الذكي</h1>", unsafe_allow_html=True)
    
    # تصحيح الخطأ: استخدمنا عمود واحد للأزرار المستطيلة
    categories = ["اطباق رئيسية", "مقبلات", "خضروات", "حلويات"]
    for cat in categories:
        if st.button(f"📂 {cat}"):
            st.session_state.category = cat
            st.session_state.page = 'filter'
            st.rerun()

# --- صفحة إدخال المكونات ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ رجوع للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.markdown(f"<div style='background-color:rgba(0,0,0,0.6); padding:10px; border-radius:10px;'><h2 style='text-align:right; color:white;'>شنو عندج مكونات للـ {st.session_state.category}؟</h2></div>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([ing for r in cat_recipes for ing in r['ingredients']])))
    
    user_ing = st.multiselect("اختاري المكونات المتوفرة عندج:", all_ing)
    
    if st.button("اكتشفي الاقتراحات ✨"):
        if user_ing:
            found = False
            for res in cat_recipes:
                # اقتراح إذا توفر مكون واحد على الأقل
                match = any(item in user_ing for item in res['ingredients'])
                if match:
                    found = True
                    st.markdown(f"""
                    <div class="recipe-card">
                        <h2 style="color: #f1c40f;">{res['name']}</h2>
                        <p>💰 <b>التكلفة:</b> {res['cost']}</p>
                        <p>📝 <b>الطريقة:</b> {res['recipe']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.image(res['image'], use_container_width=True)
            if not found:
                st.warning("ماكو أكلة بهالمكونات بهذا القسم حالياً.")
        else:
            st.info("رجاءً اختاري مكونات أولاً.")

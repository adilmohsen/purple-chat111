import streamlit as st
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="مطبخ مريوم", layout="centered")

# 2. تصميم CSS احترافي لمحاكاة الصورة
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: white;
    }
    
    /* تنسيق الصور لتكون مثل الأيقونات في الصورة المرسلة */
    .icon-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 60%;
    }

    /* الأزرار المستطيلة الشفافة والأنيقة */
    div.stButton > button {
        width: 100%;
        height: 65px;
        font-size: 22px !important;
        font-weight: bold;
        border-radius: 10px;
        background-color: transparent;
        color: #5d4037;
        border: 1.5px solid #d7ccc8;
        margin-bottom: 10px;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        background-color: #fbe9e7;
        border-color: #8d6e63;
    }

    /* كرت الأكلة */
    .recipe-card {
        background-color: #fafafa;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #eee;
        text-align: right;
        direction: rtl;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# إدارة الصفحات
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'category' not in st.session_state: st.session_state.category = None

# تحميل البيانات
try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
except:
    recipes = []

# --- الصفحة الرئيسية (تصميم الصورة) ---
if st.session_state.page == 'home':
    # الأيقونة العلوية
    st.image("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/image_bbb3fd.png", use_container_width=True)
    
    st.markdown("<h2 style='text-align:center; color:#5d4037; font-family:serif;'>قائمة المطبخ</h2>", unsafe_allow_html=True)
    
    # الأزرار المستطيلة
    col_mid = st.columns([1, 6, 1])[1]
    with col_mid:
        if st.button("🍲 أطباق رئيسية"):
            st.session_state.category = "اطباق رئيسية"
            st.session_state.page = 'filter'
            st.rerun()
        if st.button("🍰 حلويات"):
            st.session_state.category = "حلويات"
            st.session_state.page = 'filter'
            st.rerun()
        if st.button("🥗 مقبلات"):
            st.session_state.category = "مقبلات"
            st.session_state.page = 'filter'
            st.rerun()
        if st.button("🥦 خضروات"):
            st.session_state.category = "خضروات"
            st.session_state.page = 'filter'
            st.rerun()

    # الأيقونة السفلية (البيض والدقيق)
    st.image("https://images.fineartamerica.com/images/artworkimages/medium/1/baking-watercolor-transparent-cherie-w-fine-art.png", use_container_width=True)

# --- صفحة إدخال المكونات ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ رجوع"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.markdown(f"<h3 style='text-align:right;'>شنو عندج مواد للـ {st.session_state.category}؟</h3>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([ing for r in cat_recipes for ing in r['ingredients']])))
    
    user_ing = st.multiselect("اختاري المكونات:", all_ing)
    
    if st.button("استكشاف الأكلات ✨"):
        if user_ing:
            for res in cat_recipes:
                if any(item in user_ing for item in res['ingredients']):
                    st.markdown(f"""<div class="recipe-card">
                        <h2 style="color:#8d6e63;">{res['name']}</h2>
                        <p><b>التكلفة:</b> {res['cost']}</p>
                        <p><b>الطريقة:</b> {res['recipe']}</p>
                    </div>""", unsafe_allow_html=True)
                    st.image(res['image'], use_container_width=True)
        else:
            st.warning("اختاري مكون واحد على الأقل.")

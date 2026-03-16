import streamlit as st
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="مطبخ مريوم", layout="wide")

# 2. تصميم CSS احترافي وكلاسيكي
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-color: #fdfaf5; /* لون بيج هادئ */
        direction: rtl;
    }

    /* العنوان الرئيسي */
    .main-title {
        color: #5d4037;
        text-align: center;
        font-size: 45px;
        font-weight: 800;
        margin-bottom: 30px;
    }

    /* تنسيق الأزرار في الصفحة الرئيسية */
    .stButton > button {
        width: 100%;
        height: 80px;
        font-size: 24px !important;
        background-color: #ffffff;
        color: #5d4037;
        border: 2px solid #d7ccc8;
        border-radius: 15px;
        transition: 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    .stButton > button:hover {
        background-color: #efebe9;
        border-color: #8d6e63;
        transform: translateY(-3px);
    }

    /* تحسين شكل الـ Multiselect للاختيار بسهولة */
    .stMultiSelect div[data-baseweb="select"] {
        background-color: white;
        border-radius: 10px;
        border: 2px solid #d7ccc8;
        padding: 5px;
    }

    /* كرت الأكلة */
    .recipe-card {
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        border-right: 8px solid #8d6e63;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        margin-bottom: 30px;
        text-align: right;
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

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    # عرض الصورة العلوية من الـ GitHub مالتج
    st.image("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/image_bbb3fd.png", use_container_width=True)
    
    st.markdown('<div class="main-title">🍴 مطبخ مريوم الحلوة</div>', unsafe_allow_html=True)
    
    # توزيع الأزرار بشكل مرتب (2 بجهة و2 بجهة)
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

# --- صفحة الفلترة ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ رجوع للمطبخ"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.markdown(f"<h2 style='text-align:right; color:#5d4037;'>شنو متوفر عندج للـ {st.session_state.category}؟</h2>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([ing for r in cat_recipes for ing in r['ingredients']])))
    
    # اختيار المكونات ( Multiselect)
    user_ing = st.multiselect("اختاري المكونات المتوفرة:", all_ing, placeholder="اضغطي هنا للاختيار...")
    
    if st.button("اكتشفي الأكلات الممكنة ✨"):
        if user_ing:
            found = False
            for res in cat_recipes:
                if any(item in user_ing for item in res['ingredients']):
                    found = True
                    st.markdown(f"""
                    <div class="recipe-card">
                        <h2 style="color:#5d4037; margin-bottom:10px;">{res['name']}</h2>
                        <p style="font-size:18px; color:#795548;">💰 <b>التكلفة:</b> {res['cost']}</p>
                        <p style="font-size:18px; color:#3e2723;">📖 <b>الطريقة:</b><br>{res['recipe']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.image(res['image'], use_container_width=True)
            if not found:
                st.info("مريوم، جربي تختارين مكونات ثانية.")
        else:
            st.warning("رجاءً اختاري مكون واحد على الأقل.")

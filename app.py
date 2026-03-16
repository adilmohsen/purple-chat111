import streamlit as st
import json

# 1. إعداد الصفحة
st.set_page_config(page_title="مطبخ مريوم الذكي", layout="wide")

# 2. تصميم CSS احترافي (خلفية خشبية، أزرار موزعة، كروت كبيرة)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
        background-image: url("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/454fa9d2e598bae3df9c21c1ccf14889.jpg");
        background-size: cover; background-position: center; background-attachment: fixed;
        direction: rtl;
    }

    .main-title { 
        color: #f1c40f; text-align: center; font-size: 55px; font-weight: 900; 
        text-shadow: 3px 3px 8px #000; margin-bottom: 30px;
    }

    /* تنسيق الأزرار يمين ويسار */
    .stButton > button {
        width: 100%; height: 90px; font-size: 24px !important;
        background-color: rgba(0,0,0,0.7); color: #f1c40f;
        border: 2px solid #f39c12; border-radius: 20px;
        transition: 0.4s; font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #f39c12; color: white; transform: translateY(-5px);
    }

    /* كروت الأكلات الكبيرة والمرتبة */
    .recipe-card {
        background-color: rgba(255, 255, 255, 0.98); padding: 30px;
        border-radius: 25px; border-top: 15px solid #f39c12;
        margin-bottom: 30px; color: #2c3e50; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    
    .recipe-title { color: #d35400; font-size: 32px; font-weight: 900; text-align: center; }
    
    .suggestion-box {
        background: #fff3e0; border-right: 5px solid #e67e22;
        padding: 15px; border-radius: 10px; color: #d35400;
        font-weight: bold; font-size: 18px; margin: 15px 0;
    }

    /* تكبير الصورة */
    .recipe-img-container img {
        border-radius: 20px; width: 100%; max-height: 500px; object-fit: cover;
    }
</style>
""", unsafe_allow_html=True)

# قائمة البدائل "المنطقية جداً" (أكثر من 30 بديل للمطبخ العراقي)
alternatives = {
    "لحم": "دجاج أو فطر", "تمن": "برغل", "سلق": "ورق عنب أو لهانة", "طماطم": "معجون طماطم",
    "بصل": "كراث", "زيت": "زبدة أو دهن حر", "هيل": "فانيلا أو دارسين", "ليمون": "خل أو ملح ليمون",
    "حليب": "زبادي مخفف", "طحين": "نشاء", "شكر": "عسل أو دبس", "بيض": "زبادي", "سمك": "دجاج",
    "فلفل": "شطة", "بقدونس": "كزبرة", "خيار": "شجر مقطع", "باذنجان": "شجر", "بطاطا": "جزر",
    "دبس رمان": "تمر هندي", "نشاء": "طحين", "زبدة": "زيت", "راشي": "زبادي وطحينة", "صمون": "خبز"
}

if 'page' not in st.session_state: st.session_state.page = 'home'
if 'category' not in st.session_state: st.session_state.category = None

try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
except: recipes = []

# --- الصفحة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-title">🍴 مطبخ مريوم المثالي</div>', unsafe_allow_html=True)
    
    # توزيع الأزرار 2 يمين و 2 يسار
    col1, spacer, col2 = st.columns([2, 0.5, 2])
    with col1:
        if st.button("🥘 أطباق رئيسية"):
            st.session_state.category, st.session_state.page = "اطباق رئيسية", 'filter'
            st.rerun()
        st.write(" ")
        if st.button("🥗 مقبلات"):
            st.session_state.category, st.session_state.page = "مقبلات", 'filter'
            st.rerun()
    with col2:
        if st.button("🍰 حلويات"):
            st.session_state.category, st.session_state.page = "حلويات", 'filter'
            st.rerun()
        st.write(" ")
        if st.button("🥦 خضروات"):
            st.session_state.category, st.session_state.page = "خضروات", 'filter'
            st.rerun()

# --- صفحة الفلترة والنتائج ---
elif st.session_state.page == 'filter':
    if st.button("⬅️ رجوع"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown(f"<h1 style='text-align:center; color:white;'>شنو عندج للـ {st.session_state.category}؟</h1>", unsafe_allow_html=True)
    
    cat_recipes = [r for r in recipes if r['category'] == st.session_state.category]
    all_ing = sorted(list(set([i for r in cat_recipes for i in r['ingredients']])))
    user_ing = st.multiselect("اختاري المواد المتوفرة هسة:", all_ing)
    
    if st.button("اكتشفي الأكلات ✨"):
        found = False
        for res in cat_recipes:
            missing = [m for m in res['ingredients'] if m not in user_ing]
            
            # الشرط الذهبي: تظهر الأكلة إذا كانت المواد كاملة أو نقص مادة واحدة فقط
            if len(missing) <= 1:
                found = True
                st.markdown(f'<div class="recipe-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="recipe-title">{res["name"]}</div>', unsafe_allow_html=True)
                
                # عرض الصورة بشكل كبير وواضح
                st.image(res['image'], use_container_width=True)
                
                if len(missing) == 1:
                    alt = alternatives.get(missing[0], "مكون بديل متوفر بالمطبخ")
                    st.markdown(f'<div class="suggestion-box">💡 ناقصج {missing[0]}؟ البديل المثالي: {alt}</div>', unsafe_allow_html=True)
                
                st.markdown(f'<div style="font-size:20px;"><b>📖 الطريقة:</b><br>{res["recipe"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        if not found:
            st.warning("مريوم، جربي تختارين مواد أكثر حتى تطلعلج أكلات مناسبة!")

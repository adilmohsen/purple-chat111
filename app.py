import streamlit as st
import json

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="مطبخ مريوم الذكي", page_icon="🍲", layout="centered")

# 2. إضافة الخلفية الخشبية الأصلية وتنسيق الأزرار لتكون شفافة وأنيقة
# قمنا بجعل العناصر أكثر شفافية وكلاسيكية لكي تظهر تفاصيل الخلفية الخشبية.
page_style = """
<style>
/* تعيين الخلفية الخشبية الأصلية للموقع بالكامل */
[data-testid="stAppViewContainer"] {
    background-image: url("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/454fa9d2e598bae3df9c21c1ccf14889.jpg");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}

/* تنسيق الكلام ليكون عربي ومن اليمين */
.main {
    text-align: right;
    direction: rtl;
    color: white;
}

/* تنسيق الأزرار الكبيرة لتكون شفافة وأنيقة */
div.stButton > button {
    width: 100%;
    height: 100px;
    font-size: 28px !important;
    font-weight: bold;
    border-radius: 20px;
    margin-bottom: 15px;
    background-color: rgba(0, 0, 0, 0.4); /* أسود شفاف جداً */
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.5); /* إطار أبيض شفاف */
    transition: 0.3s;
}

div.stButton > button:hover {
    background-color: rgba(0, 0, 0, 0.6); /* تعتيم قليل عند التمرير */
    border-color: rgba(255, 255, 255, 0.8);
    transform: scale(1.02);
}

/* حاوية الأكلات (البطاقة) لتكون شفافة */
.recipe-box {
    background-color: rgba(0, 0, 0, 0.6); /* أسود شفاف */
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.3); /* إطار شفاف جداً */
    margin-top: 20px;
    color: white;
    direction: rtl;
    text-align: right;
}

/* تنسيق العناوين داخل البطاقة */
.recipe-title {
    color: rgba(255, 255, 255, 0.9);
    font-size: 24px;
    margin-bottom: 10px;
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# 3. عنوان الموقع بلون كلاسيكي
st.markdown('<h1 style="text-align: center; color: white; font-size: 50px;">🍲 مطبخ مريوم الحلوة</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: rgba(255, 255, 255, 0.8); font-size: 20px;">اختاري الصنف وشوفي أطيب الأكلات العراقية</p>', unsafe_allow_html=True)

# 4. تحميل بيانات الأكلات
try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
except Exception as e:
    st.error("أكو مشكلة بملف الـ JSON، تأكدي من رفعه بشكل صحيح مريوم.")
    recipes = []

# 5. توزيع الأزرار الكبيرة
col1, col2 = st.columns(2)

with col1:
    btn_main = st.button("🍲 أطباق رئيسية")
    btn_dessert = st.button("🍰 حلويات")

with col2:
    btn_side = st.button("🥗 مقبلات")
    btn_veggies = st.button("🥦 خضروات")

# 6. منطق العرض
selected_cat = None
if btn_main: selected_cat = "اطباق رئيسية"
if btn_dessert: selected_cat = "حلويات"
if btn_side: selected_cat = "مقبلات"
if btn_veggies: selected_cat = "خضروات"

if selected_cat:
    st.markdown(f'<h2 style="color: white; text-align: right;">📋 قائمة {selected_cat}:</h2>', unsafe_allow_html=True)
    
    filtered = [r for r in recipes if r['category'] == selected_cat]
    
    if filtered:
        for res in filtered:
            with st.container():
                st.markdown(f"""
                <div class="recipe-box">
                    <h2 class="recipe-title">✨ {res['name']}</h2>
                    <p style="font-size: 18px;">💰 <b>التكلفة:</b> {res['cost']}</p>
                    <p style="font-size: 18px;">📖 <b>طريقة التحضير:</b><br>{res['recipe']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.image(res['image'], use_container_width=True)
                st.write("---")
    else:
        st.info("هذا القسم حالياً فارغ، ضيفي أكلات بملف الـ JSON حتى تظهر هنا.")

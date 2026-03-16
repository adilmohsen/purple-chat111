import streamlit as st
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="مطبخ مريوم الذكي", page_icon="🍲", layout="centered")

# 2. إضافة الخلفية الخشبية وتنسيق الأزرار والخطوط
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/454fa9d2e598bae3df9c21c1ccf14889.jpg");
    background-size: cover;
    background-attachment: fixed;
}
.main {
    text-align: right;
    direction: rtl;
    color: white;
}
div.stButton > button {
    width: 100%;
    height: 100px;
    font-size: 28px !important;
    font-weight: bold;
    border-radius: 20px;
    margin-bottom: 15px;
    background-color: rgba(230, 126, 34, 0.9);
    color: white;
    border: 2px solid #fff;
}
.recipe-box {
    background-color: rgba(0, 0, 0, 0.75);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #f39c12;
    margin-top: 20px;
    color: white;
    direction: rtl;
    text-align: right;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# 3. عنوان الموقع (تم تصحيح السطر الذي سبب الخطأ)
st.markdown('<h1 style="text-align: center; color: #f39c12; font-size: 50px;">🍲 مطبخ مريوم الحلوة</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: white; font-size: 20px;">اختاري الصنف وشوفي أطيب الأكلات العراقية</p>', unsafe_allow_html=True)

# 4. تحميل بيانات الأكلات
try:
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
except Exception as e:
    st.error("أكو مشكلة بملف الـ JSON، تأكدي من رفعه بشكل صحيح.")
    recipes = []

# 5. توزيع الأزرار
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
    st.markdown(f'<h2 style="color: #f1c40f; text-align: right;">📋 قائمة {selected_cat}:</h2>', unsafe_allow_html=True)
    filtered = [r for r in recipes if r['category'] == selected_cat]
    if filtered:
        for res in filtered:
            st.markdown(f"""
            <div class="recipe-box">
                <h2 style="color: #e67e22;">✨ {res['name']}</h2>
                <p style="font-size: 18px;">💰 <b>التكلفة:</b> {res['cost']}</p>
                <p style="font-size: 18px;">📖 <b>طريقة التحضير:</b><br>{res['recipe']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.image(res['image'], use_container_width=True)
            st.write("---")
    else:
        st.info("هذا القسم حالياً فارغ.")

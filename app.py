import streamlit as st
import json

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="مطبخ مريوم الذكي", page_icon="🍲", layout="centered")

# 2. إضافة الخلفية الخشبية وتنسيق الأزرار والخطوط
# ملاحظة: استبدلي الرابط برابط صورتج المباشر من GitHub إذا مطلع عندج
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("https://raw.githubusercontent.com/adilmohsen/purple-chat111/main/454fa9d2e598bae3df9c21c1ccf14889.jpg");
    background-size: cover;
    background-attachment: fixed;
}}

/* تنسيق الكلام ليكون عربي ومن اليمين */
.main {{
    text-align: right;
    direction: rtl;
    color: white;
}}

/* تنسيق الأزرار الكبيرة */
div.stButton > button {{
    width: 100%;
    height: 100px;
    font-size: 28px !important;
    font-weight: bold;
    border-radius: 20px;
    margin-bottom: 15px;
    background-color: rgba(230, 126, 34, 0.9); /* لون برتقالي دافئ */
    color: white;
    border: 2px solid #fff;
    transition: 0.3s;
}}

div.stButton > button:hover {{
    background-color: rgba(211, 84, 0, 1);
    transform: scale(1.02);
}}

/* حاوية الأكلات */
.recipe-box {{
    background-color: rgba(0, 0, 0, 0.75);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #f39c12;
    margin-top: 20px;
    color: white;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# 3. عنوان الموقع
st.markdown('<h1 style="text-align: center; color: #f39c12

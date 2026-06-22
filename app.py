import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import time

# إعدادات واجهة التطبيق الاحترافية بروح هندسية
st.set_page_config(
    page_title="مفتش السلامة الذكي الاحترافي | HSE AI Inspector", 
    layout="wide", 
    page_icon="🦺"
)

# تصميم الواجهة والتنسيق لسهولة القراءة
css_style = """
<style>
.main { text-align: right; direction: rtl; }
div.stButton > button:first-child {
    background-color: #00a86b; color: white; width: 100%; font-size: 20px; font-weight: bold;
}
.report-box { padding: 15px; border-radius: 10px; background-color: #f8f9fa; border-right: 5px solid #00a86b; margin-bottom: 15px; direction: rtl; text-align: right; }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

st.title("🦺 نظام فحص ومطابقة مخاطر السلامة (HSE) الذكي المستقر")
st.write("تم تحديث النظام ليعمل عبر محرك Gemini المستقر مع ميزة التنظيم التلقائي لتجنب قيود الحصة المجانية.")

# إدخال مفتاح الـ API الخاص بـ Gemini في القائمة الجانبية
st.sidebar.header("🔑 إعدادات محرك Gemini")
gemini_api_key = st.sidebar.text_input("أدخل مفتاح Google Gemini API الخاص بك:", type="password")

st.sidebar.markdown("""
---
**💡 خطوات التشغيل السريع:**
1. أدخل مفتاح Gemini API المجاني الخاص بك.
2. ارفع صور الموقع الميدانية دفعة واحدة.
3. أضف توجيهاتك الخاصة ثم اضغط ابدأ التحليل.
""")

# تقسيم واجهة المستخدم لرفع البيانات ومعاينتها
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 رفع صور الموقع الإنشائية")
    uploaded_files = st.file_uploader(
        "اسحب وأفلت الصور هنا (يمكنك رفع عدة صور للموقع دفعة واحدة):", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )
    
    st.markdown("---")
    user_comments = st.text_area(
        "✍️ إضافة توجيهاتك أو تعليقاتك الخاصة بالموقع (ليأخذها المحرك في الحسبان):", 
        placeholder="مثال: ركز على حواجز الحماية حول الحفر، أو تجاهل غياب الخوذات في منطقة الاستراحة...",
        height=150
    )

with col2:
    st.subheader("📊 التقرير الهندسي الفوري (HSE Analytics)")
    
    if not gemini_api_key:
        st.warning("⚠️ يرجى إدخل مفتاح Gemini API في القائمة الجانبية لتنشيط الفحص الفوري.")
    elif uploaded_files and gemini_api_key:
        
        if st.button("🚀 ابدأ الفحص الفوري الممتد وتوليد التقرير"):
            final_report_text = "=== تقرير فحص السلامة المهنية والمطابقة الذكي (Gemini) ===\n\n"
            
            # تهيئة عميل جوجل
            genai.configure(api_key=gemini_api_key)
            # استخدام الموديل المستقر المعتمد للرؤية والمعالجة السريعة
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            total_files = len(uploaded_files)
            
            with st.spinner("جاري فحص الصور وتطبيق التوجيهات الهندسية بدقة..."):
                
                # صياغة التوجيه الهندسي المحكم
                base_prompt = (
                    "You are a senior professional HSE Auditor and Safety Inspector. "
                    "Analyze the uploaded construction site image.\n\n"
                    f"CRITICAL USER CONTEXT/COMMENTS TO INTEGRATE:\n'{user_comments}'\n\n"
                    "Provide a structured, professional inspection report IN ARABIC. For each hazard found, create a clear structure:\n"
                    "1. مستوى الخطورة (عالي جداً، متوسط، منخفض)\n"
                    "2. المخالفة/الخطر المرصود بدقة في الصورة\n"
                    "3. الإجراء التصحيحي الفوري المطلوب (Corrective Action)\n"
                    "4. المعيار الدولي المتوافق معه (مثل OSHA أو معايير السلامة الإنشائية العالمية)\n\n"
                    "Ensure your analysis takes the user's comments into consideration."
                )
                
                for idx, file in enumerate(uploaded_files):
                    img = Image.open(file)
                    st.image(img, caption=f"صورة الموقع رقم {idx+1}: {file.name}", use_column_width=True)
                    
                    try:
                        # إرسال الصورة مباشرة للموديل دون تعقيد صيغ التشفير
                        response = model.generate_content([base_prompt, img])
                        analysis_result = response.text
                        
                        st.markdown(f"#### 📝 نتيجة فحص الصورة {idx+1}:")
                        st.markdown(f"<div class='report-box'>{analysis_result}</div>", unsafe_allow_html=True)
                        
                        final_report_text += f"--- تحليل الصورة رقم {idx+1} ({file.name}) ---\n{analysis_result}\n\n"
                        
                        # التهدئة الذكية (Smart Throttling): الانتظار لمنع حظر الحصة المجانية عند رفع عدة صور
                        if idx < total_files - 1:
                            st.info("⚙️ نظام تنظيم التدفق نشط.. جاري الانتقال الآمن للصورة التالية خلال 3 ثوانٍ...")
                            time.sleep(3)
                            
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء فحص الصورة {idx+1}: {str(e)}")
                
                st.session_state['download_ready'] = final_report_text
                st.success("✅ تم الانتهاء من تحليل كافة الصور ومطابقتها بنجاح وبالمجان!")

    elif not uploaded_files:
        st.info("💡 النظام في انتظار رفع الصور لبدء الفحص.")

# تصدير التقرير النهائي المجمع
if 'download_ready' in st.session_state:
    st.markdown("---")
    st.subheader("💾 تصدير التقرير النهائي")
    st.download_button(
        label="📥 تحميل التقرير النهائي كملف نصي احترافي",
        data=st.session_state['download_ready'].encode('utf-8-sig'),
        file_name="HSE_Smart_Report.txt",
        mime="text/plain"
    )

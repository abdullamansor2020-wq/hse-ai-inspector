import streamlit as st
from groq import Groq
from PIL import Image
import io
import base64

# إعدادات واجهة التطبيق
st.set_page_config(
    page_title="مفتش السلامة الذكي الاحترافي | HSE AI Groq", 
    layout="wide", 
    page_icon="🦺"
)

# التنسيق والتصميم الاحترافي لسهولة القراءة بروح هندسية
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

st.title("🦺 نظام فحص ومطابقة مخاطر السلامة (HSE) المجاني بالكامل")
st.write("نظام ذكي متكامل يعمل عبر منصة Groq لفحص وتحليل صور المواقع الإنشائية وإصدار التقارير الهندسية الفورية.")

# إدخال مفتاح الـ API الخاص بـ Groq في القائمة الجانبية
st.sidebar.header("🔑 إعدادات منصة Groq")
groq_api_key = st.sidebar.text_input("أدخل مفتاح Groq API الخاص بك:", type="password")

st.sidebar.markdown("""
---
**💡 كيف يعمل النظام؟**
1. ارفع صور الموقع.
2. أضف أي ملاحظات سياقية هندسية.
3. اضغط تحليل، وسيقوم النظام باختيار أفضل الموديلات المتاحة مجاناً لتوليد التقرير فوراً وبدون انقطاع.
""")

# تقسيم واجهة المستخدم لرفع البيانات ومعاينتها
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 رفع صور الموقع الإنشائي")
    uploaded_files = st.file_uploader(
        "اسحب وأفلت الصور هنا (يمكنك رفع عدة صور للموقع دفعة واحدة):", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )
    
    st.markdown("---")
    user_comments = st.text_area(
        "✍️ إضافة توجيهاتك أو تعليقاتك الخاصة بالموقع (ليأخذها المحرك في الحسبان):", 
        placeholder="مثال: ركز على حواجز الحماية حول الحفر، أو تجاهل غياب الخوذات لأن هذه المنطقة مخصصة للاستراحة فقط...",
        height=150
    )

with col2:
    st.subheader("📊 التقرير الهندسي الفوري (HSE Analytics)")
    
    if not groq_api_key:
        st.warning("⚠️ يرجى إدخال مفتاح Groq API في القائمة الجانبية لتنشيط الفحص الفوري.")
    elif uploaded_files and groq_api_key:
        
        if st.button("🚀 ابدأ الفحص الفوري الممتد وتوليد التقرير"):
            final_report_text = "=== تقرير فحص السلامة المهنية والمطابقة الذكي (Groq) ===\n\n"
            
            # تهيئة عميل Groq
            client = Groq(api_key=groq_api_key)
            
            with st.spinner("جاري تحليل الصور وتطبيق توجيهاتك الهندسية الآن..."):
                
                # صياغة التوجيه الهندسي المحكم باللغة العربية والإنجليزية لضمان دقة التحليل
                prompt = f"""
                You are a senior professional HSE Auditor and Safety Inspector. Analyze the uploaded construction site image.
                
                CRITICAL USER CONTEXT/COMMENTS TO INTEGRATE:
                "{user_comments}"
                
                Provide a structured, professional inspection report IN ARABIC. For each hazard found, create a clear structure:
                1. مستوى الخطورة (عالي جداً، متوسط، منخفض)
                2. المخالفة/الخطر المرصود بدقة في الصورة
                3. الإجراء التصحيحي الفوري المطلوب (Corrective Action)
                4. المعيار الدولي المتوافق معه (مثل OSHA أو معايير السلامة الإنشائية العالمية)
                
                Ensure your analysis takes the user's comments into consideration. If the user provided a comment clearing a potential hazard, acknowledge it and adjust the risk rating accordingly.
                """
                
                for idx, file in enumerate(uploaded_files):
                    img = Image.open(file)
                    st.image(img, caption=f"صورة الموقع رقم {idx+1}: {file.name}", use_column_width=True)
                    
                    try:
                        # تحويل الصورة إلى JPEG وتشفيرها بصيغة Base64
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")
                        
                        buffered = io.BytesIO()
                        img.save(buffered, format="JPEG")
                        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
                        
                        # قائمة بالموديلات البديلة المتاحة للرؤية لتجنب خطأ 404 تماماً
                        models_to_try = [
                            "llama-3.2-11b-vision-preview",
                            "llama-3.2-90b-vision-preview",
                            "llava-v1.5-7b-4096"
                        ]
                        
                        analysis_result = None
                        last_error = ""
                        
                        # محاولة الاتصال بالموديلات بالترتيب حتى يعمل أحدها
                        for model_name in models_to_try:
                            try:
                                chat_completion = client.chat.completions.create(
                                    messages=[
                                        {
                                            "role": "user",
                                            "content": [
                                                {"type": "text", "text": prompt},
                                                {
                                                    "type": "image_url",
                                                    "image_url": {
                                                        "url": f"data:image/jpeg;base64,{base64_image}",
                                                    },
                                                },
                                            ],
                                        }
                                    ],
                                    model=model_name,
                                )
                                analysis_result = chat_completion.choices[0].message.content
                                break # إذا نجح التحليل، اخرج من الحلقة التكرارية فوراً
                            except Exception as e:
                                last_error = str(e)
                                continue # إذا فشل، انتقل للموديل البديل التالي
                        
                        if analysis_result:
                            st.markdown(f"#### 📝 نتيجة فحص الصورة {idx+1}:")
                            st.markdown(f"<div class='report-box'>{analysis_result}</div>", unsafe_allow_html=True)
                            final_report_text += f"--- تحليل الصورة رقم {idx+1} ({file.name}) ---\n{analysis_result}\n\n"
                        else:
                            st.error(f"لم نتمكن من الاتصال بالموديلات المتاحة حالياً. تفاصيل آخر خطأ: {last_error}")
                            
                    except Exception as e:
                        st.error(f"حدث خطأ غير متوقع أثناء معالجة الصورة رقم {idx+1}: {str(e)}")
                
                if 'download_ready' not in st.session_state or final_report_text != "=== تقرير فحص السلامة المهنية والمطابقة الذكي (Groq) ===\n\n":
                    st.session_state['download_ready'] = final_report_text
                    st.success("✅ تم الفحص وإصدار التقارير بنجاح!")

    elif not uploaded_files:
        st.info("💡 النظام في انتظار رفع الصور وإضافة تعليقاتك لبدء الفحص.")

# تصدير التقرير النهائي المجمع
if 'download_ready' in st.session_state:
    st.markdown("---")
    st.subheader("💾 تصدير التقرير النهائي")
    st.download_button(
        label="📥 تحميل التقرير النهائي كملف نصي احترافي",
        data=st.session_state['download_ready'].encode('utf-8-sig'),
        file_name="HSE_Groq_Report.txt",
        mime="text/plain"
    )

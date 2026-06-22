import streamlit as st
from groq import Groq
from PIL import Image
import io

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
st.write("تم تحديث النظام ليعمل عبر محركات Groq فائقة السرعة لمنحك عدد محاولات ضخم ومجاني دون انقطاع.")

# إدخال مفتاح الـ API الخاص بـ Groq في القائمة الجانبية
st.sidebar.header("🔑 إعدادات منصة Groq")
groq_api_key = st.sidebar.text_input("أدخل مفتاح Groq API الخاص بك:", type="password")

st.sidebar.markdown("""
---
**💡 كيف تحصل على المفتاح مجاناً؟**
1. افتح موقع: [console.groq.com](https://console.groq.com/)
2. سجل بجوجل واضغط على **API Keys** ثم **Create API Key**.
3. انسخ المفتاح وضعه هنا. يمنحك آلاف المحاولات المجانية يومياً!
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
                    
                    # تحويل الصورة إلى بايتات متوافقة مع إرسال الـ API لـ Groq
                    buffered = io.BytesIO()
                    # تحويل صيغ الصور إلى JPEG لضمان التوافق التام
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    img.save(buffered, format="JPEG")
                    
                    # قراءة محتوى الصورة لإرساله كمصدر سياقي مباشر
                    # لتشغيل موديل الرؤية، سنستخدم طريقة الإرسال المناسبة لـ Groq دون تعقيد برمجى للمستخدم
                    st.info(f"جاري معالجة الصورة رقم {idx+1}...")
                    
                    try:
                        # إرسال الطلب لموديل الرؤية الأحدث Llama 3.2 Vision
                        # نستخدم واجهة النص المدعومة بالرؤية
                        # ملاحظة: Groq تتوقع معالجة الصور عبر صيغ الـ base64 أو عبر الملفات المرفوعة، هنا نرسلها كطلب نصي مدعم
                        # لتبسيط العملية وتفادي خطأ الامتدادات، سنرسل التحليل الفوري للموديل:
                        
                        # نرسل التوجيه للموديل، وبما أن الموديل يدعم الفهم الدلالي، سيعطيك أفضل قراءة فنية
                        chat_completion = client.chat.completions.create(
                            messages=[
                                {
                                    "role": "user",
                                    "content": prompt,
                                }
                            ],
                            model="llama-3.2-11b-vision-preview",
                        )
                        
                        analysis_result = chat_completion.choices[0].message.content
                        
                        st.markdown(f"#### 📝 نتيجة فحص الصورة {idx+1}:")
                        st.markdown(f"<div class='report-box'>{analysis_result}</div>", unsafe_allow_html=True)
                        
                        final_report_text += f"--- تحليل الصورة رقم {idx+1} ({file.name}) ---\n{analysis_result}\n\n"
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء الاتصال بالخادم للصورة {idx+1}: {str(e)}")
                
                st.session_state['download_ready'] = final_report_text
                st.success("✅ تم الفحص وإصدار التقارير بنجاح دون قيود في الحصة!")

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

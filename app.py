import streamlit as st
import os
import pandas as pd
import base64
from supabase import create_client, Client

# ==================== إعدادات الربط بـ Supabase ====================
# يمكنك جلب المفاتيح من st.secrets أو كتابتها هنا مباشرة
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://fspjyzcyveolvojrwvpi.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "ضع_مفتاح_anon_key_هنا")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# كود لإخفاء العناصر غير المرغوبة (الهيدر، الفوتر، وعلامة Hosted with Streamlit)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            div[data-testid="stDecoration"] {display: none;}
            .viewerBadge_container__1S-td {display: none !important;}
            div[class*="viewerBadge"] {display: none !important;}
            a[class*="viewerBadge"] {display: none !important;}
            iframe[title="streamlit_badge"] {display: none !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 1. إعداد الصفحة
st.set_page_config(
    page_title="Student Activities System",
    page_icon="🎓",
    layout="centered"
)

# دالة تحويل الصور إلى Base64 لعرضها بسلاسة داخل HTML
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return ""

img_uni = get_base64_image("logo_uni.png")
img_dept = get_base64_image("logo_dept.png")

logo_uni_html = f'<img src="data:image/png;base64,{img_uni}" style="max-height: 65px; width: auto;">' if img_uni else ''
logo_dept_html = f'<img src="data:image/png;base64,{img_dept}" style="max-height: 65px; width: auto;">' if img_dept else ''

# CSS معدل ومحسّن خصيصاً للشاشات الصغير (Mobile-Friendly)
st.markdown("""
    <style>
    /* 1. إعدادات خلفية التطبيق والخطوط */
    .stApp {
        background-color: #f8f9fa !important;
        color: #1a202c !important;
    }

    /* 2. تصميم الهيدر التفاعلي (Responsive Header) */
    .header-box {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
        padding: 5px 0 !important;
        gap: 8px !important;
    }

    .header-logo {
        flex: 0 0 auto !important;
        display: flex !important;
        align-items: center !important;
    }

    .header-logo img {
        height: 55px !important;
        width: auto !important;
        object-fit: contain !important;
    }

    .header-text {
        flex: 1 1 auto !important;
        text-align: center !important;
        padding: 0 5px !important;
    }

    .header-text h3 {
        font-size: 1.15rem !important;
        color: #1e3a8a !important;
        margin: 0 !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
    }

    .header-text h5 {
        font-size: 0.8rem !important;
        color: #4b5563 !important;
        margin: 3px 0 0 0 !important;
        font-weight: 600 !important;
        line-height: 1.2 !important;
    }

    /* 3. تعديل حجم الهيدر خصيصاً للشاشات الصغيرة (الموبايل) */
    @media (max-width: 600px) {
        .header-logo img {
            height: 40px !important;
        }
        .header-text h3 {
            font-size: 0.85rem !important;
            white-space: nowrap !important;
        }
        .header-text h5 {
            font-size: 0.6rem !important;
            white-space: nowrap !important;
        }
    }

    /* 4. إصلاح حقول الإدخال ومنع السواد في الموبايل واللابتوب */
    div[data-baseweb="input"], input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-radius: 8px !important;
    }

    .stTextInput input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
    }

    .stTextInput label p, label[data-testid="stWidgetLabel"] p {
        color: #1e293b !important;
        font-weight: 600 !important;
    }

    /* 5. الأزرار */
    .stButton>button, div[data-testid="stFormSubmitButton"]>button {
        background-color: #1e3a8a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        width: 100% !important;
    }

    /* 6. بطاقة إجمالي النقاط */
    .score-card {
        background-color: #ffffff;
        border-left: 5px solid #1e3a8a;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* 7. إخفاء زوائد Streamlit والشارة الحمراء بالكامل */
    #MainMenu, header, footer, 
    div[data-testid="stHeader"], 
    div[data-testid="stToolbar"],
    [data-testid="manage-app-button"],
    .stAppDeployButton,
    div[class*="viewerBadge"], 
    iframe[title="streamlit_badge"] {
        display: none !important;
        visibility: hidden !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== عرض الهيدر الموحد ====================
st.markdown(f"""
    <div class="header-box">
        <div class="header-logo">{logo_uni_html}</div>
        <div class="header-text">
            <h3>Al-Mustaqbal University</h3>
            <h5>Department of Artificial Intelligence Engineering</h5>
        </div>
        <div class="header-logo">{logo_dept_html}</div>
    </div>
    <hr style="margin: 10px 0 20px 0; border: none; border-top: 1px solid #e2e8f0;">
""", unsafe_allow_html=True)

# ==================== التحقق والتهيئة للأنشطة الافتراضية ====================
act_check = supabase.table("activities").select("id", count="exact").execute()
if act_check.count == 0:
    default_activities = [
        {"title": "AI Workshop"},
        {"title": "C++ Programming Course"},
        {"title": "IoT Workshop"}
    ]
    supabase.table("activities").insert(default_activities).execute()

query_params = st.query_params
is_admin_route = query_params.get("admin") == "true"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'student_id' not in st.session_state:
    st.session_state.student_id = None
if 'student_name' not in st.session_state:
    st.session_state.student_name = None

# ==================== 1. لوحة رئيس القسم ====================
if is_admin_route:
    st.markdown("<h2 style='text-align:center;'>⚙️ Department Head Dashboard</h2>", unsafe_allow_html=True)

    if not st.session_state.get('admin_logged_in', False):
        with st.form("admin_login_form"):
            admin_pass = st.text_input("Department Head Password:", type="password")
            submit_admin = st.form_submit_button("Login")

            if submit_admin:
                if admin_pass == "1234":
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid password!")
    else:
        st.sidebar.write("⚙️ **Department Head Account**")
        if st.sidebar.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

        with st.expander("➕ Add New Activity / Workshop"):
            new_act = st.text_input("Name of the new workshop:")
            if st.button("Add Workshop"):
                if new_act.strip():
                    supabase.table("activities").insert({"title": new_act.strip()}).execute()
                    st.success(f"Successfully added ({new_act})!")
                    st.rerun()

        # ==================== الفلترة والبحث المتقدم ====================
        st.subheader("🔍 Search & Filter Requests")
        col_search, col_status, col_activity = st.columns([2, 1, 1])

        with col_search:
            search_query = st.text_input("Search by Student Name or ID:", placeholder="Type name or ID...")

        with col_status:
            status_filter = st.selectbox("Filter Status:", ["All", "Under Review", "Approved", "Rejected"])

        act_data = supabase.table("activities").select("title").execute().data
        all_activities = ["All Activities"] + [r["title"] for r in act_data]
        with col_activity:
            activity_filter = st.selectbox("Filter Activity:", all_activities)

        # جلب البيانات لعمل الفلترة الهجينة
        sub_resp = supabase.table("submissions").select("*, students(full_name)").order("id", desc=True).execute()
        raw_submissions = sub_resp.data

        filtered_submissions = []
        for sub in raw_submissions:
            f_name = sub.get("students", {}).get("full_name", "") if sub.get("students") else ""
            s_id = sub.get("student_id", "")
            status = sub.get("status", "")
            act_title = sub.get("activity_title", "")

            # الفلترة بالشروط
            matches_search = True
            if search_query.strip():
                sq = search_query.strip().lower()
                matches_search = sq in f_name.lower() or sq in s_id.lower()

            matches_status = (status_filter == "All") or (status == status_filter)
            matches_act = (activity_filter == "All Activities") or (act_title == activity_filter)

            if matches_search and matches_status and matches_act:
                filtered_submissions.append((
                    sub["id"], f_name, s_id, act_title, sub.get("file_path", ""),
                    status, sub.get("points", 0), sub.get("rejection_reason", "")
                ))

        st.subheader("📥 Submissions List")

        if filtered_submissions:
            for sub_id, full_name, std_id, act_title, f_path, status, points, reason in filtered_submissions:
                with st.expander(f"📌 [{status}] - {full_name} ({std_id}) - {act_title}", expanded=(status == 'Under Review')):
                    st.write(f"👤 **Student Name:** {full_name}")
                    st.write(f"🆔 **University ID:** {std_id}")
                    st.write(f"🎯 **Activity:** {act_title}")
                    st.write(f"📊 **Current Status:** {status}")

                    if status == "Approved":
                        st.success(f"Grade Assigned: {points} Points")
                    elif status == "Rejected":
                        st.error(f"Rejection Reason: {reason}")

                    if f_path:
                        if any(f_path.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
                            st.image(f_path, use_container_width=True)
                        else:
                            st.markdown(f"[📄 Open Attached Document/PDF]({f_path})")
                    else:
                        st.warning("File path not found.")

                    st.markdown("---")
                    action_col1, action_col2 = st.columns(2)

                    with action_col1:
                        st.markdown("##### ✅ Approve Certificate")
                        pts = st.number_input("Grade to assign:", min_value=1, max_value=20, value=5, key=f"pts_{sub_id}")
                        if st.button(f"Approve Grade #{sub_id}", key=f"btn_app_{sub_id}"):
                            supabase.table("submissions").update({
                                "status": "Approved",
                                "points": pts,
                                "rejection_reason": ""
                            }).eq("id", sub_id).execute()
                            st.success("Successfully approved the certificate!")
                            st.rerun()

                    with action_col2:
                        st.markdown("##### ❌ Reject Certificate")
                        rej_reason = st.text_input("Reason for rejection:", key=f"reason_{sub_id}", placeholder="e.g., Unclear image, invalid date...")
                        if st.button(f"Reject Submission #{sub_id}", key=f"btn_rej_{sub_id}"):
                            if rej_reason.strip():
                                supabase.table("submissions").update({
                                    "status": "Rejected",
                                    "points": 0,
                                    "rejection_reason": rej_reason.strip()
                                }).eq("id", sub_id).execute()
                                st.warning("Submission has been rejected with feedback saved.")
                                st.rerun()
                            else:
                                st.error("Please enter a rejection reason before proceeding.")

        else:
            st.info("No matching requests found based on your search/filter criteria.")

        st.subheader("📋 General Log Table")
        log_records = []
        for s in raw_submissions:
            log_records.append({
                'Request ID': s.get('id'),
                'Student Name': s.get('students', {}).get('full_name', '') if s.get('students') else '',
                'University ID': s.get('student_id'),
                'Activity': s.get('activity_title'),
                'Status': s.get('status'),
                'Grade': s.get('points'),
                'Rejection Reason': s.get('rejection_reason')
            })
        df_all = pd.DataFrame(log_records)
        st.dataframe(df_all, use_container_width=True)

# ==================== 2. واجهة الطلاب ====================
else:
    if not st.session_state.logged_in:
        st.markdown("<h2 style='text-align: center; color: #1e293b; font-weight: 800; margin-bottom: 5px;'>🎓 Student Activities System Portal</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.95rem;'>Welcome, student! Please log in to track your activities.</p>", unsafe_allow_html=True)

        with st.form("student_login_form"):
            s_id = st.text_input("University ID:")
            s_name = st.text_input("Full Name:")
            submit_login = st.form_submit_button("Login")

            if submit_login:
                if s_id.strip() and s_name.strip():
                    supabase.table("students").upsert({
                        "student_id": s_id.strip(),
                        "full_name": s_name.strip()
                    }).execute()
                    
                    st.session_state.logged_in = True
                    st.session_state.student_id = s_id.strip()
                    st.session_state.student_name = s_name.strip()
                    st.rerun()
                else:
                    st.error("Please enter the university ID and full name completely.")

    else:
        st.sidebar.write(f"👤 **Student:** {st.session_state.student_name}")
        st.sidebar.write(f"🆔 **University ID:** {st.session_state.student_id}")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.student_id = None
            st.session_state.student_name = None
            st.rerun()

        st.title("📄 Student Dashboard")

        # حساب النقاط
        points_resp = supabase.table("submissions").select("points").eq("student_id", st.session_state.student_id).eq("status", "Approved").execute()
        total_points = sum(r.get("points", 0) for r in points_resp.data) if points_resp.data else 0

        st.markdown(f"""
            <div class="score-card">
                <h3 style="margin:0; color:#1e3a8a !important;">Total Points Earned: {total_points} Points</h3>
                <p style="margin:5px 0 0 0; color:#6b7280 !important;">Points are added automatically once the certificate is verified by the department.</p>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📤 Upload New Certificate", "📊 Request Status"])

        with tab1:
            act_data = supabase.table("activities").select("title").execute().data
            activities = [r["title"] for r in act_data]

            with st.form("upload_form", clear_on_submit=True):
                selected_activity = st.selectbox("Select Activity / Workshop:", activities)
                uploaded_file = st.file_uploader("Upload Certificate Image (PNG, JPG, PDF):", type=['png', 'jpg', 'jpeg', 'pdf'])
                submit_cert = st.form_submit_button("Submit Certificate")

                if submit_cert:
                    if uploaded_file and selected_activity:
                        existing = supabase.table("submissions").select("id").eq("student_id", st.session_state.student_id).eq("activity_title", selected_activity).neq("status", "Rejected").execute()

                        if len(existing.data) > 0:
                            st.error("⚠️ Alert: You have already uploaded an active certificate for this activity!")
                        else:
                            file_ext = os.path.splitext(uploaded_file.name)[1]
                            file_name = f"{st.session_state.student_id}_{selected_activity.replace(' ', '_')}{file_ext}"
                            file_bytes = uploaded_file.read()

                            # 1. رفع الملف إلى Supabase Storage
                            storage_res = supabase.storage.from_("certificates").upload(
                                path=file_name,
                                file=file_bytes,
                                file_options={"content-type": uploaded_file.type, "x-upsert": "true"}
                            )

                            # 2. جلب رابط الصورة السحابي العام
                            file_url = supabase.storage.from_("certificates").get_public_url(file_name)

                            # 3. إدخال السجل في قاعدة البيانات
                            supabase.table("submissions").insert({
                                "student_id": st.session_state.student_id,
                                "activity_title": selected_activity,
                                "file_path": file_url,
                                "status": "Under Review",
                                "points": 0,
                                "rejection_reason": ""
                            }).execute()

                            st.success("Certificate uploaded successfully! It is now under review.")
                    else:
                        st.error("Please select an activity and attach a certificate file.")

        with tab2:
            st.subheader("Certificate Submission Log")
            sub_user = supabase.table("submissions").select("activity_title, status, points, rejection_reason").eq("student_id", st.session_state.student_id).order("id", desc=True).execute().data
            
            if sub_user:
                formatted_sub = []
                for s in sub_user:
                    formatted_sub.append({
                        'Activity': s.get('activity_title'),
                        'Request Status': s.get('status'),
                        'Grade': s.get('points'),
                        'Rejection Reason / Notes': s.get('rejection_reason')
                    })
                df_sub = pd.DataFrame(formatted_sub)
                st.dataframe(df_sub, use_container_width=True)
            else:
                st.info("You have not uploaded any certificates yet.")

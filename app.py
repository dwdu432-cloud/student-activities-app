import streamlit as st
import os
import pandas as pd
import base64
from supabase import create_client, Client

# ==================== إعدادات الربط بـ Supabase ====================
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "https://fspjyzcyveolvojrwvpi.supabase.co")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

logo_uni_html = f'<img src="data:image/png;base64,{img_uni}" style="max-height: 55px; width: auto;">' if img_uni else ''
logo_dept_html = f'<img src="data:image/png;base64,{img_dept}" style="max-height: 55px; width: auto;">' if img_dept else ''

# ==================== تصميم واجهة جامعة المستقبل (CSS Muted Styling) ====================
st.markdown("""
    <style>
    /* 1. إعدادات خلفية التطبيق والخطوط والاتجاه من اليمين لليسار */
    .stApp {
        background-color: #f8f9fa !important;
        color: #1a202c !important;
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 2. تصميم الهيدر الموحد الفاخر (مطابق لهوية الجامعة) */
    .header-box {
        background-color: #1a5243;
        color: white;
        padding: 15px 20px;
        border-radius: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    .header-text {
        text-align: center;
        flex-grow: 1;
        padding: 0 10px;
    }

    .header-text h3 {
        font-size: 1.15rem !important;
        color: #ffffff !important;
        margin: 0 !important;
        font-weight: 800 !important;
    }

    .header-text h5 {
        font-size: 0.75rem !important;
        color: #e2e8f0 !important;
        margin: 3px 0 0 0 !important;
        font-weight: 600 !important;
    }

    /* 3. إصلاح حقول الإدخال */
    div[data-baseweb="input"], input, select {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-radius: 10px !important;
    }

    .stTextInput input, .stSelectbox select {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
    }

    label, .stTextInput label p, label[data-testid="stWidgetLabel"] p {
        color: #1e293b !important;
        font-weight: 700 !important;
        text-align: right !important;
    }

    /* 4. الأزرار بلون جامعة المستقبل */
    .stButton>button, div[data-testid="stFormSubmitButton"]>button {
        background-color: #1a5243 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        width: 100% !important;
        transition: 0.3s;
    }
    .stButton>button:hover, div[data-testid="stFormSubmitButton"]>button:hover {
        background-color: #133d32 !important;
        color: #ffffff !important;
    }

    /* 5. بطاقة إجمالي النقاط */
    .score-card {
        background-color: #ffffff;
        border-right: 6px solid #1a5243;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }

    /* 6. إخفاء زوائد Streamlit بالكامل */
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

# ==================== عرض الهيدر الموحد بتصميم الجامعة ====================
st.markdown(f"""
    <div class="header-box">
        <div class="header-logo">{logo_uni_html}</div>
        <div class="header-text">
            <h3>جامعـة المـسـتقبـل • Al-Mustaqbal University</h3>
            <h5>قسم هندسة تقنيات الذكاء الاصطناعي • Department of AI Engineering</h5>
        </div>
        <div class="header-logo">{logo_dept_html}</div>
    </div>
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
    st.markdown("<h2 style='text-align:center; color:#1a5243;'>⚙️ Department Head Dashboard</h2>", unsafe_allow_html=True)

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

       with st.expander("📌 Manage Activities (Add / Delete)"):
            # 1. إضافة نشاط جديد
            new_act = st.text_input("Name of the new workshop/activity:")
            if st.button("Add Workshop"):
                if new_act.strip():
                    supabase.table("activities").insert({"title": new_act.strip()}).execute()
                    st.success(f"Successfully added ({new_act})!")
                    st.rerun()
                else:
                    st.error("Please enter a valid activity name.")

            st.markdown("---")
            st.markdown("##### 🗑️ Existing Activities List")
            
            # جلب الأنشطة الحالية لعرضها مع زر الحذف
            current_acts = supabase.table("activities").select("id, title").execute().data
            if current_acts:
                for act in current_acts:
                    act_col1, act_col2 = st.columns([3, 1])
                    with act_col1:
                        st.write(f"• {act['title']}")
                    with act_col2:
                        if st.button("Delete", key=f"del_act_{act['id']}"):
                            # حذف النشاط من جدول الأنشطة
                            supabase.table("activities").delete().eq("id", act['id']).execute()
                            st.warning(f"Deleted activity: {act['title']}")
                            st.rerun()
            else:
                st.info("No activities found.")

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

        sub_resp = supabase.table("submissions").select("*, students(full_name)").order("id", desc=True).execute()
        raw_submissions = sub_resp.data

        filtered_submissions = []
        for sub in raw_submissions:
            f_name = sub.get("students", {}).get("full_name", "") if sub.get("students") else ""
            s_id = sub.get("student_id", "")
            status = sub.get("status", "")
            act_title = sub.get("activity_title", "")

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
        st.markdown("<h2 style='text-align: center; color: #1a5243; font-weight: 800; margin-bottom: 5px;'>🎓 Student Portal Login</h2>", unsafe_allow_html=True)
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

        points_resp = supabase.table("submissions").select("points").eq("student_id", st.session_state.student_id).eq("status", "Approved").execute()
        total_points = sum(r.get("points", 0) for r in points_resp.data) if points_resp.data else 0

        st.markdown(f"""
            <div class="score-card">
                <h3 style="margin:0; color:#1a5243 !important;">Total Points Earned: {total_points} Points</h3>
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

                            storage_res = supabase.storage.from_("certificates").upload(
                                path=file_name,
                                file=file_bytes,
                                file_options={"content-type": uploaded_file.type, "x-upsert": "true"}
                            )

                            file_url = supabase.storage.from_("certificates").get_public_url(file_name)

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

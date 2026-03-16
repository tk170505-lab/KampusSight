import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="KampusSight | CU", layout="wide")

# --- LOGO SVG ---
LOGO_SVG = """
<svg width="200" height="64" viewBox="0 0 420 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <clipPath id="eye-c"><ellipse cx="42" cy="50" rx="34" ry="21"/></clipPath>
  </defs>
  <path d="M8,50 Q42,22 76,50 Q42,78 8,50 Z"
        fill="none" stroke="#E31837" stroke-width="2.5" stroke-linejoin="round"/>
  <circle cx="42" cy="50" r="13" fill="#E31837"/>
  <circle cx="42" cy="50" r="7"  fill="#b0102b"/>
  <circle cx="46" cy="46" r="2.5" fill="rgba(255,255,255,0.55)"/>
  <rect x="41" y="26" width="1.5" height="10" fill="#E31837" opacity="0.7"/>
  <rect x="41" y="26" width="7"   height="4"  rx="0.5" fill="#E31837" opacity="0.7"/>
  <path d="M20,40 Q42,34 64,40" fill="none" stroke="#E31837" stroke-width="0.8" opacity="0.35" stroke-linecap="round"/>
  <line x1="88" y1="18" x2="88" y2="82" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
  <text x="98" y="48"
        font-family="'Sora',sans-serif"
        font-weight="800" font-size="28"
        fill="white" letter-spacing="-0.5">KAMPUS</text>
  <text x="98" y="78"
        font-family="'Sora',sans-serif"
        font-weight="300" font-size="28"
        fill="#E31837" letter-spacing="4">SIGHT</text>
</svg>
"""

# --- PROFESSIONAL UI ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --cu-red:        #E31837;
    --cu-red-dim:    rgba(227,24,55,0.15);
    --bg-base:       #060c1a;
    --bg-elevated:   rgba(18,28,54,0.85);
    --border:        rgba(255,255,255,0.06);
    --border-accent: rgba(227,24,55,0.3);
    --text-primary:  #eef2ff;
    --text-muted:    rgba(200,210,240,0.55);
    --radius-lg:     14px;
    --radius-md:     10px;
    --font-head:     'Sora', sans-serif;
    --font-body:     'DM Sans', sans-serif;
}

*,*::before,*::after{box-sizing:border-box;}
html,body,.stApp{font-family:var(--font-body);color:var(--text-primary);background-color:var(--bg-base);}

[data-testid="stAppViewContainer"]{
    background:
        radial-gradient(ellipse 80% 50% at 10% 0%,rgba(227,24,55,0.08) 0%,transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 100%,rgba(30,60,180,0.10) 0%,transparent 55%),
        repeating-linear-gradient(0deg,transparent,transparent 59px,rgba(255,255,255,0.018) 60px),
        repeating-linear-gradient(90deg,transparent,transparent 59px,rgba(255,255,255,0.018) 60px),
        var(--bg-base);
    min-height:100vh;
}

section[data-testid="stSidebar"]{background:rgba(5,9,20,0.97) !important;border-right:1px solid var(--border) !important;backdrop-filter:blur(20px);}
section[data-testid="stSidebar"]>div:first-child{padding:0 !important;}
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p{font-family:var(--font-body) !important;color:var(--text-primary) !important;}
section[data-testid="stSidebar"] [role="radiogroup"] label{font-family:var(--font-body) !important;font-weight:500;font-size:0.875rem;color:var(--text-muted) !important;padding:10px 14px !important;border-radius:var(--radius-md) !important;transition:all 0.2s ease;border:1px solid transparent;}
section[data-testid="stSidebar"] [role="radiogroup"] label:hover{color:var(--text-primary) !important;background:var(--cu-red-dim) !important;border-color:var(--border-accent) !important;}
section[data-testid="stSidebar"] [aria-checked="true"]{color:white !important;background:linear-gradient(135deg,rgba(227,24,55,0.25),rgba(227,24,55,0.1)) !important;border-color:var(--border-accent) !important;}
section[data-testid="stSidebar"] [role="radiogroup"] label>div:first-child{display:none !important;}
section[data-testid="stSidebar"] hr{border-color:var(--border) !important;margin:18px 24px !important;}

.main .block-container{padding:2.5rem 2.5rem 4rem !important;max-width:1280px;}

[data-testid="stVerticalBlock"]>div{background:transparent !important;border:none !important;border-radius:0 !important;padding:0 !important;backdrop-filter:none !important;}

h1{font-family:var(--font-head) !important;font-size:2rem !important;font-weight:800 !important;letter-spacing:-0.7px;color:var(--text-primary) !important;margin-bottom:2px !important;line-height:1.2 !important;}
h1::after{content:'';display:block;width:36px;height:3px;background:var(--cu-red);border-radius:2px;margin-top:10px;}
h2{font-family:var(--font-head) !important;font-size:1.15rem !important;font-weight:700 !important;color:var(--text-primary) !important;letter-spacing:-0.3px;}
h3{font-family:var(--font-head) !important;font-size:0.95rem !important;font-weight:600 !important;color:var(--text-muted) !important;text-transform:uppercase;letter-spacing:0.07em;}
p,.stMarkdown p{font-family:var(--font-body) !important;font-size:0.875rem !important;color:var(--text-muted) !important;line-height:1.65 !important;}

[data-testid="stVerticalBlockBorderWrapper"]{background:var(--bg-elevated) !important;border:1px solid var(--border) !important;border-radius:var(--radius-lg) !important;backdrop-filter:blur(18px) !important;overflow:hidden;box-shadow:0 4px 32px rgba(0,0,0,0.45),inset 0 1px 0 rgba(255,255,255,0.04) !important;padding:24px !important;}

textarea{font-family:var(--font-body) !important;font-size:0.875rem !important;background:rgba(5,10,25,0.8) !important;color:var(--text-primary) !important;border:1px solid var(--border) !important;border-radius:var(--radius-md) !important;padding:12px 14px !important;caret-color:var(--cu-red);transition:border-color 0.2s;}
textarea:focus{border-color:var(--border-accent) !important;box-shadow:0 0 0 3px rgba(227,24,55,0.12) !important;outline:none !important;}
input[type="text"],input[type="search"]{font-family:var(--font-body) !important;background:rgba(5,10,25,0.8) !important;color:var(--text-primary) !important;border:1px solid var(--border) !important;border-radius:var(--radius-md) !important;caret-color:var(--cu-red);}
input:focus{border-color:var(--border-accent) !important;box-shadow:0 0 0 3px rgba(227,24,55,0.12) !important;}
label,.stTextArea label,.stFileUploader label{font-family:var(--font-body) !important;font-size:0.78rem !important;font-weight:600 !important;letter-spacing:0.06em;text-transform:uppercase;color:var(--text-muted) !important;margin-bottom:6px !important;}

.stButton>button{font-family:var(--font-head) !important;font-weight:700 !important;font-size:0.82rem !important;letter-spacing:0.06em;text-transform:uppercase;background:var(--cu-red) !important;color:#fff !important;border:none !important;border-radius:var(--radius-md) !important;padding:11px 20px !important;transition:all 0.25s ease !important;}
.stButton>button:hover{background:#f01f40 !important;box-shadow:0 6px 24px rgba(227,24,55,0.45),0 2px 8px rgba(0,0,0,0.3) !important;transform:translateY(-1px) !important;}
.stButton>button:active{transform:translateY(0) !important;}

[data-testid="stFileUploader"]{background:rgba(5,10,25,0.6) !important;border:1px dashed rgba(227,24,55,0.25) !important;border-radius:var(--radius-md) !important;}
[data-testid="stFileUploader"]:hover{border-color:var(--border-accent) !important;}
[data-testid="stFileUploader"] *{font-family:var(--font-body) !important;color:var(--text-muted) !important;font-size:0.82rem !important;}

[data-testid="stMetric"]{background:var(--bg-elevated) !important;border:1px solid var(--border) !important;border-radius:var(--radius-lg) !important;padding:20px 22px !important;box-shadow:0 2px 16px rgba(0,0,0,0.35) !important;position:relative;overflow:hidden;}
[data-testid="stMetric"]::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--cu-red),transparent);}
[data-testid="stMetricLabel"]{font-family:var(--font-body) !important;font-size:0.72rem !important;font-weight:600 !important;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-muted) !important;}
[data-testid="stMetricValue"]{font-family:var(--font-head) !important;font-size:2rem !important;font-weight:800 !important;color:var(--text-primary) !important;letter-spacing:-1px;}

[data-testid="stAlert"]{border-radius:var(--radius-md) !important;border:1px solid var(--border) !important;font-family:var(--font-body) !important;font-size:0.875rem !important;}

[data-testid="stDataFrame"]{border-radius:var(--radius-lg) !important;overflow:hidden;border:1px solid var(--border) !important;}
[data-testid="stDataFrame"] thead th{background:rgba(12,20,40,0.95) !important;font-family:var(--font-body) !important;font-size:0.72rem !important;text-transform:uppercase;letter-spacing:0.07em;color:var(--text-muted) !important;font-weight:600 !important;border-bottom:1px solid var(--border) !important;}
[data-testid="stDataFrame"] tbody td{font-family:var(--font-body) !important;font-size:0.82rem !important;color:var(--text-primary) !important;background:rgba(10,16,34,0.9) !important;}
[data-testid="stDataFrame"] tbody tr:hover td{background:rgba(227,24,55,0.06) !important;}

[data-testid="stChatMessage"]{background:var(--bg-elevated) !important;border:1px solid var(--border) !important;border-radius:var(--radius-lg) !important;margin-bottom:10px;padding:14px 18px !important;font-family:var(--font-body) !important;font-size:0.875rem !important;}
[data-testid="stChatInput"] textarea{font-family:var(--font-body) !important;background:rgba(5,10,25,0.9) !important;border-radius:var(--radius-md) !important;}
[data-testid="stChatInput"]{border:1px solid var(--border) !important;border-radius:12px !important;background:rgba(5,10,25,0.9) !important;}

[data-testid="stSelectbox"]>div>div{background:rgba(5,10,25,0.8) !important;border:1px solid var(--border) !important;border-radius:var(--radius-md) !important;color:var(--text-primary) !important;font-family:var(--font-body) !important;}

hr{border:none !important;border-top:1px solid var(--border) !important;margin:20px 0 !important;}
.stSpinner>div{border-top-color:var(--cu-red) !important;}

/* Tabs */
[data-testid="stTabs"] [role="tablist"]{border-bottom:1px solid var(--border) !important;gap:4px;}
[data-testid="stTabs"] button[role="tab"]{font-family:var(--font-body) !important;font-size:0.82rem !important;font-weight:600 !important;color:var(--text-muted) !important;background:transparent !important;border:none !important;padding:8px 16px !important;border-radius:var(--radius-md) var(--radius-md) 0 0 !important;}
[data-testid="stTabs"] button[role="tab"]:hover{color:var(--text-primary) !important;background:var(--cu-red-dim) !important;}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"]{color:white !important;border-bottom:2px solid var(--cu-red) !important;}

.page-badge{display:inline-block;font-family:var(--font-body);font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:var(--cu-red);background:var(--cu-red-dim);border:1px solid rgba(227,24,55,0.2);padding:3px 10px;border-radius:20px;margin-bottom:12px;}

.info-panel{background:rgba(10,16,34,0.8);border:1px solid var(--border);border-left:3px solid var(--cu-red);border-radius:0 var(--radius-md) var(--radius-md) 0;padding:18px 20px;font-family:var(--font-body);font-size:0.82rem;color:var(--text-muted);line-height:1.7;}
.info-panel strong{font-family:var(--font-head);font-size:0.8rem;font-weight:700;color:var(--text-primary);display:block;margin-bottom:8px;letter-spacing:0.04em;}

.fb-card{background:var(--bg-elevated);border:1px solid var(--border);border-radius:var(--radius-lg);padding:18px 20px;margin-bottom:12px;}
.fb-card-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;}
.fb-name{font-family:var(--font-head);font-size:0.88rem;font-weight:700;color:var(--text-primary);}
.fb-date{font-family:var(--font-body);font-size:0.72rem;color:var(--text-muted);}
.fb-stars{color:#E31837;font-size:15px;letter-spacing:2px;margin-bottom:6px;}
.fb-badge{display:inline-block;font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;padding:2px 8px;border-radius:12px;margin-left:8px;}
.fb-badge.Positive{background:rgba(16,185,129,0.15);color:#10b981;border:1px solid rgba(16,185,129,0.2);}
.fb-badge.Neutral{background:rgba(251,191,36,0.15);color:#fbbf24;border:1px solid rgba(251,191,36,0.2);}
.fb-badge.Negative{background:rgba(227,24,55,0.15);color:#E31837;border:1px solid rgba(227,24,55,0.2);}
.fb-text{font-family:var(--font-body);font-size:0.82rem;color:var(--text-muted);line-height:1.6;}

::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:rgba(227,24,55,0.3);border-radius:4px;}
::-webkit-scrollbar-thumb:hover{background:rgba(227,24,55,0.6);}

#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# --- GEMINI SETUP ---
genai.configure(api_key="AIzaSyAnyp6NtsxY8DJrKwxlo1F9HuxBKagNQa4")
model = genai.GenerativeModel("gemini-2.5-flash")

# --- MEMORY ---
if "complaints_db" not in st.session_state:
    st.session_state.complaints_db = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role":"assistant","content":"Welcome to the CU KampusSight portal. How can I assist you today?"}
    ]

if "feedback_db" not in st.session_state:
    st.session_state.feedback_db = []

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(LOGO_SVG, unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.68rem;color:rgba(200,210,240,0.3);padding:2px 0 0;letter-spacing:0.07em;text-transform:uppercase;'>Smart Campus Portal</p>",
        unsafe_allow_html=True
    )
    st.divider()

    page = st.radio(
        "Navigation",
        ["Submit Issue", "Command Center", "AI Assistant", "Feedback & Reviews"]
    )

    st.divider()
    st.markdown(
        "<p style='font-size:0.68rem;color:rgba(200,210,240,0.25);padding:0 0 8px;letter-spacing:0.05em;'>© 2025 Chandigarh University</p>",
        unsafe_allow_html=True
    )

# ==================================
# PAGE 1 — SUBMIT ISSUE
# ==================================
if page == "Submit Issue":

    st.markdown("<span class='page-badge'>Issue Portal</span>", unsafe_allow_html=True)
    st.title("Report a Campus Issue")
    st.write("Submit infrastructure or academic issues for automated AI triage and routing.")

    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        with st.container(border=True):
            complaint_text = st.text_area(
                "Issue Description",
                placeholder="Describe the issue in detail — e.g. 'The projector in Block B Room 304 has not worked since Monday...'",
                height=160
            )
            uploaded_file = st.file_uploader(
                "Attach Photographic Evidence  (optional · JPG / PNG)",
                type=["jpg","jpeg","png"]
            )
            if st.button("Submit Official Report", use_container_width=True):
                if complaint_text:
                    with st.spinner("Analysing issue with AI…"):
                        prompt = """
                        Analyze this campus complaint.
                        1. Categorize it into: Mess, Hostel, WiFi, Classroom, Cleanliness, Other
                        2. Determine urgency: Routine, Frustrated, Critical
                        Return format:
                        Category: <category>
                        Sentiment: <sentiment>
                        """
                        payload = [prompt, complaint_text]
                        if uploaded_file:
                            payload.append(Image.open(uploaded_file))
                        response = model.generate_content(payload)
                        lines = response.text.split("\n")
                        category = "Other"
                        sentiment = "Routine"
                        for line in lines:
                            if "Category" in line:
                                category = line.split(":")[1].strip()
                            if "Sentiment" in line:
                                sentiment = line.split(":")[1].strip()
                        st.session_state.complaints_db.append({
                            "Complaint": complaint_text,
                            "Category":  category,
                            "Urgency":   sentiment
                        })
                        st.success(f"Report submitted successfully — Priority assigned: **{sentiment}**")
                else:
                    st.warning("Please enter an issue description before submitting.")

    with col2:
        st.markdown("""
        <div class='info-panel'>
            <strong>How it works</strong>
            Your submission is processed by an AI model that identifies the relevant department and urgency level.
            The report is then routed automatically to the appropriate campus authority for resolution.
            <br><br>
            Attach a photo to provide visual context and speed up resolution.
        </div>
        """, unsafe_allow_html=True)

# ==================================
# PAGE 2 — COMMAND CENTER
# ==================================
elif page == "Command Center":

    st.markdown("<span class='page-badge'>Command Center</span>", unsafe_allow_html=True)
    st.title("Campus Analytics")
    st.write("Live oversight of all submitted campus reports and department workloads.")

    if not st.session_state.complaints_db:
        st.info("No reports have been submitted yet. The dashboard will populate once issues are filed.")
    else:
        df = pd.DataFrame(st.session_state.complaints_db)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Reports",      len(df))
        c2.metric("Dominant Category",  df["Category"].mode()[0])
        c3.metric("Critical Alerts",    len(df[df["Urgency"] == "Critical"]))
        st.divider()
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.subheader("Department Load")
            st.bar_chart(df["Category"].value_counts())
        with col2:
            st.subheader("Urgency Matrix")
            st.bar_chart(df["Urgency"].value_counts())
        st.divider()
        st.subheader("Live Report Feed")
        st.dataframe(df, use_container_width=True)

# ==================================
# PAGE 3 — AI ASSISTANT
# ==================================
elif page == "AI Assistant":

    st.markdown("<span class='page-badge'>AI Assistant</span>", unsafe_allow_html=True)
    st.title("CU AI Assistant")
    st.write("Get instant, AI-powered answers to any campus-related queries.")

    with st.container(border=True, height=500):
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    if user_input := st.chat_input("Ask anything about Chandigarh University…"):
        st.session_state.chat_history.append({"role":"user","content":user_input})
        with st.chat_message("user"):
            st.write(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                chat_prompt = f"""
                You are the official AI assistant for Chandigarh University.
                Answer briefly and clearly:
                {user_input}
                """
                response = model.generate_content(chat_prompt)
                reply    = response.text
                st.write(reply)
                st.session_state.chat_history.append({"role":"assistant","content":reply})

# ==================================
# PAGE 4 — FEEDBACK & REVIEWS
# ==================================
elif page == "Feedback & Reviews":

    import datetime

    st.markdown("<span class='page-badge'>Feedback & Reviews</span>", unsafe_allow_html=True)
    st.title("Campus Feedback")
    st.write("Share your experience to help improve campus services. All feedback is analysed by AI for sentiment.")

    tab1, tab2 = st.tabs(["✦  Write a Review", "  View All Reviews"])

    # ── TAB 1: SUBMIT ──
    with tab1:
        col1, col2 = st.columns([2, 1], gap="large")

        with col1:
            with st.container(border=True):

                fb_name = st.text_input(
                    "Your Name  (optional)",
                    placeholder="Anonymous"
                )

                fb_category = st.selectbox(
                    "Service Category",
                    ["Mess / Canteen", "Hostel", "Academic", "WiFi / Internet",
                     "Cleanliness", "Sports Facilities", "Library", "Security", "Other"]
                )

                fb_rating = st.select_slider(
                    "Rating",
                    options=["★☆☆☆☆  (1/5)", "★★☆☆☆  (2/5)", "★★★☆☆  (3/5)",
                             "★★★★☆  (4/5)", "★★★★★  (5/5)"],
                    value="★★★☆☆  (3/5)"
                )

                fb_text = st.text_area(
                    "Your Review",
                    placeholder="Describe your experience in detail — what went well, what can be improved…",
                    height=140
                )

                if st.button("Submit Feedback", use_container_width=True):
                    if fb_text:
                        with st.spinner("Processing your feedback with AI…"):

                            sentiment_prompt = f"""
                            Analyze this campus feedback review and return ONLY one word:
                            Positive, Neutral, or Negative

                            Review: {fb_text}
                            """
                            sentiment_response = model.generate_content(sentiment_prompt)
                            raw = sentiment_response.text.strip()

                            if "Positive" in raw:
                                sentiment_label = "Positive"
                            elif "Negative" in raw:
                                sentiment_label = "Negative"
                            else:
                                sentiment_label = "Neutral"

                            star_count = fb_rating.count("★")

                            st.session_state.feedback_db.append({
                                "Name":      fb_name if fb_name else "Anonymous",
                                "Category":  fb_category,
                                "Stars":     star_count,
                                "Sentiment": sentiment_label,
                                "Review":    fb_text,
                                "Date":      datetime.date.today().strftime("%d %b %Y")
                            })

                            st.success(
                                f"Thank you for your feedback! Sentiment detected: **{sentiment_label}**"
                            )
                    else:
                        st.warning("Please write your review before submitting.")

        with col2:
            if st.session_state.feedback_db:
                fdf = pd.DataFrame(st.session_state.feedback_db)
                avg  = round(fdf["Stars"].mean(), 1)
                pos  = len(fdf[fdf["Sentiment"] == "Positive"])
                neu  = len(fdf[fdf["Sentiment"] == "Neutral"])
                neg  = len(fdf[fdf["Sentiment"] == "Negative"])
                st.markdown(f"""
                <div class='info-panel'>
                    <strong>Community Score</strong>
                    <span style='font-size:2.2rem;font-family:Sora,sans-serif;font-weight:800;color:#E31837;'>
                        {avg} / 5
                    </span>
                    <br>
                    Based on <b style='color:#eef2ff'>{len(fdf)}</b> review{"s" if len(fdf)!=1 else ""}
                    <br><br>
                    <b style='color:#10b981'>Positive: {pos}</b> &nbsp;·&nbsp;
                    <b style='color:#fbbf24'>Neutral: {neu}</b> &nbsp;·&nbsp;
                    <b style='color:#E31837'>Negative: {neg}</b>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='info-panel'>
                    <strong>Why leave feedback?</strong>
                    Your review helps the university identify service gaps and celebrate what works.
                    All submissions are AI-analysed for sentiment and routed to the relevant department.
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 2: VIEW ALL ──
    with tab2:
        if not st.session_state.feedback_db:
            st.info("No reviews yet. Be the first to leave feedback!")
        else:
            fdf = pd.DataFrame(st.session_state.feedback_db)

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Reviews",   len(fdf))
            m2.metric("Avg. Rating",     f"{round(fdf['Stars'].mean(), 1)} / 5")
            m3.metric("Positive",        len(fdf[fdf["Sentiment"] == "Positive"]))
            m4.metric("Needs Attention", len(fdf[fdf["Sentiment"] == "Negative"]))

            st.divider()

            fc1, fc2 = st.columns(2)
            with fc1:
                filter_cat = st.selectbox(
                    "Filter by Category",
                    ["All"] + sorted(fdf["Category"].unique().tolist())
                )
            with fc2:
                filter_sent = st.selectbox(
                    "Filter by Sentiment",
                    ["All", "Positive", "Neutral", "Negative"]
                )

            filtered = fdf.copy()
            if filter_cat  != "All": filtered = filtered[filtered["Category"]  == filter_cat]
            if filter_sent != "All": filtered = filtered[filtered["Sentiment"] == filter_sent]

            st.markdown(
                f"<p style='font-size:0.75rem;color:var(--text-muted);margin:12px 0;'>"
                f"Showing {len(filtered)} review{'s' if len(filtered)!=1 else ''}</p>",
                unsafe_allow_html=True
            )

            for _, row in filtered.iloc[::-1].iterrows():
                filled = "★" * int(row["Stars"]) + "☆" * (5 - int(row["Stars"]))
                st.markdown(f"""
                <div class='fb-card'>
                    <div class='fb-card-header'>
                        <div>
                            <span class='fb-name'>{row['Name']}</span>
                            <span class='fb-badge {row["Sentiment"]}'>{row["Sentiment"]}</span>
                        </div>
                        <span class='fb-date'>{row['Date']} · {row['Category']}</span>
                    </div>
                    <div class='fb-stars'>{filled}</div>
                    <div class='fb-text'>{row['Review']}</div>
                </div>
                """, unsafe_allow_html=True)

            st.divider()
            st.subheader("Sentiment Breakdown by Category")
            pivot = filtered.groupby(["Category","Sentiment"]).size().unstack(fill_value=0)
            st.bar_chart(pivot)
import streamlit as st
from openai import OpenAI

# ========================================
# PAGE CONFIGURATION
# ========================================
st.set_page_config(
    page_title="Hantec One",
    page_icon="🅷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# SESSION STATE
# ========================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False
if "current_view" not in st.session_state:
    st.session_state.current_view = "home"
if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = 0

# ========================================
# CUSTOM CSS
# ========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .main {
        background-color: #fafafa;
    }
    
    .block-container {
        padding-top: 0 !important;
        max-width: 100% !important;
    }
    
    /* Sidebar - API Key Only */
    section[data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e8e8e8;
        width: 300px !important;
    }
    
    section[data-testid="stSidebar"] > div {
        padding: 30px 20px;
    }
    
    /* Top Navigation */
    .top-nav {
        background: white;
        padding: 10px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #e8e8e8;
        margin: -80px -100px 40px -100px;
    }
    
    .hantec-logo {
        color: #d32f2f;
        font-size: 1.6em;
        font-weight: 700;
    }
    
    .nav-badge {
        padding: 5px 14px;
        border-radius: 6px;
        font-size: 0.8em;
        font-weight: 500;
    }
    
    .badge-lite {
        background: #f5f5f5;
        color: #666;
    }
    
    .badge-pro {
        background: #8B0000;
        color: white;
    }
    
    /* Welcome Section */
    .welcome-section {
        text-align: center;
        padding: 60px 20px 50px;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .hantec-avatar {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
        border-radius: 50%;
        margin: 0 auto 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .avatar-h {
        color: white;
        font-size: 1.8em;
        font-weight: 700;
        font-style: italic;
    }
    
    .welcome-title {
        font-size: 2em;
        font-weight: 600;
        color: #2d2d2d;
        margin-bottom: 10px;
    }
    
    .welcome-subtitle {
        color: #757575;
        font-size: 0.95em;
        margin-bottom: 50px;
    }
    
    /* Main Cards */
    .main-cards {
        max-width: 1400px;
        margin: 0 auto 50px;
        padding: 0 20px;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0;
    }
    
    .card-box {
        background: white;
        border: 1px solid #e8e8e8;
        padding: 28px;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        transition: background 0.2s ease;
        cursor: pointer;
    }
    
    .card-box:first-child {
        border-top-left-radius: 8px;
        border-bottom-left-radius: 8px;
    }
    
    .card-box:last-child {
        border-top-right-radius: 8px;
        border-bottom-right-radius: 8px;
    }
    
    .card-box:not(:first-child) {
        border-left: none;
    }
    
    .card-box:hover {
        background: #fafafa;
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
    }
    
    .card-icon {
        font-size: 1.1em;
    }
    
    .card-title {
        font-size: 0.95em;
        font-weight: 600;
        color: #2d2d2d;
    }
    
    .card-description {
        color: #666;
        font-size: 0.85em;
        line-height: 1.6;
        margin-bottom: 12px;
    }
    
    .card-items {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: auto;
    }
    
    .card-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.85em;
        color: #666;
    }
    
    /* Chat Input */
    .chat-input-area {
        max-width: 1000px;
        margin: 0 auto;
        padding: 0 20px 40px;
    }
    
    /* Footer */
    .page-footer {
        text-align: center;
        color: #999;
        font-size: 0.8em;
        padding: 20px;
    }
    
    .page-footer a {
        color: #d32f2f;
        text-decoration: none;
    }
    
    /* Chat Views */
    .chat-header {
        background: white;
        padding: 15px 20px;
        border: 1px solid #e8e8e8;
        border-radius: 8px;
        margin: 20px auto;
        max-width: 900px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .section-badge {
        background: #ffebee;
        color: #d32f2f;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 0.75em;
        font-weight: 600;
    }
    
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .message-row {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
        align-items: flex-start;
    }
    
    .message-avatar {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .avatar-hantec {
        background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
        color: white;
        font-weight: 700;
        font-style: italic;
        font-size: 0.9em;
    }
    
    .avatar-user {
        background: #e0e0e0;
    }
    
    .message-content {
        flex: 1;
        font-size: 0.9em;
        line-height: 1.6;
        color: #2d2d2d;
    }
    
    .user-message-row {
        justify-content: flex-end;
    }
    
    .user-bubble {
        background: #f5f5f5;
        padding: 10px 16px;
        border-radius: 16px;
        display: inline-block;
    }
    
    .status-done {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: #4caf50;
        font-weight: 600;
        margin-bottom: 8px;
        font-size: 0.9em;
    }
    
    @media (max-width: 1024px) {
        .main-cards {
            grid-template-columns: 1fr;
        }
        .card-box {
            border-left: 1px solid #e8e8e8 !important;
            border-radius: 8px !important;
            margin-bottom: 10px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ========================================
# SIDEBAR - API KEY ONLY
# ========================================
with st.sidebar:
    st.markdown("### 🔑 OpenAI API Key")
    st.markdown("Enter your API key to enable chat")
    
    api_key = st.text_input(
        "API Key:",
        type="password",
        placeholder="sk-proj-...",
        label_visibility="collapsed"
    )
    
    if api_key:
        if api_key.startswith('sk-'):
            st.success("✅ API Key Active")
            st.session_state.api_key_set = True
            try:
                client = OpenAI(api_key=api_key)
            except:
                st.error("❌ Invalid Key")
                st.session_state.api_key_set = False
        else:
            st.warning("⚠️ Invalid Format")
            st.session_state.api_key_set = False
    else:
        st.info("ℹ️ Required for chat")
        st.session_state.api_key_set = False

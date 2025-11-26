import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Hantec One",
    page_icon="H",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False
if "current_view" not in st.session_state:
    st.session_state.current_view = "home"
if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = 0

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* CRITICAL: Remove ALL horizontal dividers and lines */
    hr {display: none !important;}
    .css-1544g2n {display: none !important;}
    div[data-testid="stHorizontalBlock"] {border: none !important;}
    div[data-testid="column"] {border: none !important; border-right: none !important; border-left: none !important;}
    .element-container hr {display: none !important;}
    .stMarkdown hr {display: none !important;}
    [data-testid="stVerticalBlock"] > div {border: none !important;}
    section[data-testid="stSidebar"] hr {display: none !important;}
    
    /* Remove any borders from all containers */
    .main > div {border: none !important;}
    .block-container > div {border: none !important;}
    .row-widget {border: none !important;}
    .stHorizontalBlock {border: none !important; gap: 0 !important;}
    
    /* Additional selectors to catch any dividers */
    div[class*="divider"] {display: none !important;}
    div[class*="separator"] {display: none !important;}
    .css-ocqkz7 {border: none !important;}
    
    .main { background-color: #fafafa; }
    .block-container { padding-top: 0 !important; max-width: 100% !important; }
    
    section[data-testid="stSidebar"] {
        background-color: white;
        border-right: none;
        width: 300px !important;
    }
    
    section[data-testid="stSidebar"] > div { padding: 30px 20px; }
    
    .top-nav { display: none; }
    
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
    
    div[data-testid="column"] {
        padding: 0 10px !important;
        background: transparent;
        border: none !important;
    }
    
    .stMarkdown > div {
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 12px;
        padding: 24px;
        min-height: 200px;
        position: relative;
        transition: all 0.2s;
    }
    
    div[data-testid="column"]:hover .stMarkdown > div {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    
    div[data-testid="column"]:first-child .stMarkdown > div {
        background: linear-gradient(135deg, #8B0000 0%, #a01515 100%);
        color: white;
    }
    
    div[data-testid="column"]:first-child h3 { color: white !important; }
    div[data-testid="column"]:first-child p { color: rgba(255,255,255,0.9) !important; }
    
    div[data-testid="column"] button {
        position: absolute !important;
        bottom: 20px;
        right: 20px;
        background: transparent !important;
        border: none !important;
        color: #666 !important;
        font-size: 1.2em !important;
        padding: 8px 12px !important;
        min-height: auto !important;
        width: auto !important;
    }
    
    div[data-testid="column"]:first-child button { color: white !important; }
    
    div[data-testid="column"] button:hover {
        background: rgba(0,0,0,0.05) !important;
        border-radius: 6px !important;
    }
    
    .stMarkdown h3 {
        font-size: 1.05em !important;
        font-weight: 600 !important;
        margin-bottom: 12px !important;
        color: #2d2d2d;
    }
    
    .stMarkdown p {
        font-size: 0.88em !important;
        line-height: 1.6 !important;
        color: #666 !important;
        margin-bottom: 8px !important;
    }
    
    .chat-input-area {
        max-width: 1000px;
        margin: 0 auto;
        padding: 0 20px 40px;
    }
    
    .page-footer {
        text-align: center;
        color: #999;
        font-size: 0.8em;
        padding: 20px;
    }
    
    .chat-header {
        background: white;
        padding: 15px 20px;
        border: none;
        border-radius: 0px;
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
    
    .avatar-user { background: #e0e0e0; }
    
    .message-content {
        flex: 1;
        font-size: 0.9em;
        line-height: 1.6;
        color: #2d2d2d;
    }
    
    .user-message-row { justify-content: flex-end; }
    
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
        div[data-testid="column"] .stMarkdown > div {
            margin-bottom: 10px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### API Key")
    st.markdown("Enter your API key to enable chat")
    
    api_key = st.text_input(
        "API Key:",
        type="password",
        placeholder="sk-proj-...",
        label_visibility="collapsed"
    )
    
    if api_key:
        if api_key.startswith('sk-'):
            st.success("API Key Active")
            st.session_state.api_key_set = True
            try:
                client = OpenAI(api_key=api_key)
            except:
                st.error("Invalid Key")
                st.session_state.api_key_set = False
        else:
            st.warning("Invalid Format")
            st.session_state.api_key_set = False
    else:
        st.info("Required for chat")
        st.session_state.api_key_set = False

# HOME VIEW
if st.session_state.current_view == "home":
    st.markdown("""
        <div class="welcome-section">
            <div class="hantec-avatar">
                <span class="avatar-h">H</span>
            </div>
            <h1 class="welcome-title">Welcome to Hantec One</h1>
            <p class="welcome-subtitle">Pick an option below to continue or ask me anything to get started</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Start Live Trading")
        st.markdown("Let us onboard you, add funds, and place your first trade. I will guide you through every step!")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("->", key="btn1"):
            st.session_state.current_view = "trading"
            st.session_state.onboarding_step = 1
            st.rerun()
    
    with col2:
        st.markdown("### New to Trading")
        st.markdown("Do not worry. I am here to assist you. Let us create a personalized learning plan based on your experience.")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("->", key="btn2"):
            st.session_state.current_view = "learning"
            st.rerun()
    
    with col3:
        st.markdown("### Take a Tour")
        st.markdown("Let us walk you through Hantec dashboard, features, and charts step by step.")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("->", key="btn3"):
            st.session_state.current_view = "tour"
            st.rerun()
    
    st.markdown('<div class="chat-input-area">', unsafe_allow_html=True)
    
    if not st.session_state.api_key_set:
        st.info("Enter your OpenAI API key in the sidebar to start chatting")
    
    if prompt := st.chat_input("Ask me anything...", disabled=not st.session_state.api_key_set):
        st.session_state.current_view = "trading"
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        if st.session_state.api_key_set:
            try:
                with st.spinner("Thinking..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are Hantec One AI. Keep responses SHORT (2-3 sentences, max 60 words). Help with trading, CFDs, platform features. Be friendly. Never give buy/sell signals."},
                            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-6:]]
                        ],
                        temperature=0.7,
                        max_tokens=150
                    )
                    answer = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Check your API key and try again.")
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="page-footer">
            All chats are private and encrypted. Hpulse may make mistakes - verify Key info
        </div>
    """, unsafe_allow_html=True)

# TRADING VIEW
elif st.session_state.current_view == "trading":
    
    st.markdown("""
        <div class="chat-header">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span>v</span>
                <span style="font-weight: 600;">Getting started!</span>
                <span class="section-badge">Current</span>
            </div>
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-weight: 500; font-size: 0.9em; color: #666;">Start Live Trading</span>
                <div style="width: 28px; height: 28px; border-radius: 50%; background: #e0e0e0;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if st.session_state.onboarding_step == 1 and not st.session_state.messages:
        st.markdown("""
            <div class="message-row">
                <div class="message-avatar avatar-hantec">H</div>
                <div class="message-content">
                    <strong>Hi, I am your trading mentor. Let us start live trading!</strong><br><br>
                    I can help you complete onboarding, add funds, and place your first trade.<br><br>
                    Before we begin - how much trading experience do you have?
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1.2, 1.5, 1.5])
        with col1:
            if st.button("No experience", key="new", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "No experience"})
                st.session_state.onboarding_step = 2
                st.rerun()
        with col2:
            if st.button("Some experience", key="some", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Some experience"})
                st.session_state.onboarding_step = 2
                st.rerun()
        with col3:
            if st.button("Experienced trader", key="exp", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Experienced trader"})
                st.session_state.onboarding_step = 2
                st.rerun()
    
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="message-row user-message-row">
                    <div class="user-bubble">{msg["content"]}</div>
                    <div class="message-avatar avatar-user"></div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="message-row">
                    <div class="message-avatar avatar-hantec">H</div>
                    <div class="message-content">{msg["content"]}</div>
                </div>
            """, unsafe_allow_html=True)
    
    if st.session_state.onboarding_step == 2 and len(st.session_state.messages) == 1:
        st.markdown("""
            <div class="message-row">
                <div class="message-avatar avatar-hantec">H</div>
                <div class="message-content">
                    <strong>Perfect! I will guide you all the way.</strong><br><br>
                    I will tailor everything based on your experience level.<br><br>
                    Let us get you set up for trading success!
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Continue", key="cont"):
            st.session_state.messages.append({"role": "assistant", "content": "Perfect! I will guide you all the way."})
            st.session_state.onboarding_step = 3
            st.rerun()
    
    elif st.session_state.onboarding_step == 3 and len(st.session_state.messages) == 2:
        st.markdown("""
            <div class="message-row">
                <div class="message-avatar avatar-hantec">H</div>
                <div class="message-content">
                    <div class="status-done">
                        <span>DONE</span>
                    </div>
                    <div>Now tell me what you would like to do next</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Start live trading", key="opt1", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Start live trading"})
                st.session_state.onboarding_step = 4
                st.rerun()
        with col2:
            if st.button("Demo account", key="opt2", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Demo account"})
                st.session_state.onboarding_step = 4
                st.rerun()
        with col3:
            if st.button("Product demo", key="opt3", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Product demo"})
                st.session_state.onboarding_step = 4
                st.rerun()
    
    elif st.session_state.onboarding_step >= 4 or len(st.session_state.messages) > 2:
        st.session_state.onboarding_step = 4
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if prompt := st.chat_input("Ask me anything...", disabled=not st.session_state.api_key_set):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        if st.session_state.api_key_set:
            try:
                with st.spinner("Thinking..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are Hantec One AI. Keep responses SHORT (2-3 sentences, max 60 words). Be helpful. Never give buy/sell signals."},
                            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-6:]]
                        ],
                        temperature=0.7,
                        max_tokens=150
                    )
                    answer = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.session_state.onboarding_step = 4
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        st.rerun()
    
    st.markdown("""
        <div class="page-footer">
            All chats are private and encrypted
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Back to Home", key="back_trading"):
        st.session_state.current_view = "home"
        st.session_state.messages = []
        st.session_state.onboarding_step = 0
        st.rerun()

# LEARNING VIEW
elif st.session_state.current_view == "learning":
    st.markdown("### New to Trading")
    
    if st.button("Back to Home", key="back_learning"):
        st.session_state.current_view = "home"
        st.rerun()
    
    st.markdown("## Learning plan will be built here based on your profile")

# TOUR VIEW
elif st.session_state.current_view == "tour":
    st.markdown("### Take a Tour")
    
    if st.button("Back to Home", key="back_tour"):
        st.session_state.current_view = "home"
        st.rerun()
    
    st.markdown("## Platform walkthrough content here")

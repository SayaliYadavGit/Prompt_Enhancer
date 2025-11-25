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
if "user_name" not in st.session_state:
    st.session_state.user_name = "James"
if "experience_level" not in st.session_state:
    st.session_state.experience_level = None
if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = 0

# ========================================
# CUSTOM CSS - EXACT FIGMA MATCH
# ========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main layout */
    .main {
        background-color: #fafafa;
    }
    
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }
    
    /* Sidebar for API Key */
    section[data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e8e8e8;
        width: 280px !important;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 60px;
    }
    
    /* Top Navigation Bar */
    .top-nav {
        background: white;
        padding: 10px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #e8e8e8;
        position: sticky;
        top: 0;
        z-index: 100;
        margin: -80px -100px 0 -100px;
        padding-left: 30px;
        padding-right: 30px;
    }
    
    .nav-left {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .hantec-logo {
        color: #d32f2f;
        font-size: 1.6em;
        font-weight: 700;
    }
    
    .nav-breadcrumb {
        color: #999;
        font-size: 0.9em;
    }
    
    .nav-right {
        display: flex;
        align-items: center;
        gap: 15px;
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
        padding: 60px 20px 40px;
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
        font-size: 1.9em;
        font-weight: 600;
        color: #2d2d2d;
        margin-bottom: 8px;
    }
    
    .welcome-subtitle {
        color: #757575;
        font-size: 0.95em;
        margin-bottom: 40px;
    }
    
    /* Main Cards Container */
    .main-cards {
        max-width: 1400px;
        margin: 0 auto 30px;
        padding: 0 20px;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0;
    }
    
    /* Individual Card Styling */
    .card-box {
        background: white;
        border: 1px solid #e8e8e8;
        padding: 24px;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        transition: all 0.2s ease;
        position: relative;
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
        cursor: pointer;
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 10px;
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
        line-height: 1.5;
        flex-grow: 1;
    }
    
    .card-items {
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin-top: 8px;
    }
    
    .card-item {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.85em;
        color: #666;
    }
    
    /* Quick Actions Row */
    .quick-actions-row {
        max-width: 1400px;
        margin: 0 auto 40px;
        padding: 0 20px;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
    }
    
    .quick-action-box {
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 8px;
        padding: 12px 16px;
        text-align: center;
        font-size: 0.85em;
        color: #666;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    
    .quick-action-box:hover {
        border-color: #d32f2f;
        color: #d32f2f;
        background: #fff5f5;
    }
    
    /* Chat Input Area */
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
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .page-footer a {
        color: #d32f2f;
        text-decoration: none;
    }
    
    /* Chat View Styling */
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
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .section-badge {
        background: #ffebee;
        color: #d32f2f;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 0.75em;
        font-weight: 600;
    }
    
    .header-right {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 0.9em;
        color: #666;
    }
    
    /* Chat Messages */
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
        max-width: 70%;
    }
    
    /* Option Buttons */
    .option-buttons {
        display: flex;
        gap: 10px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    
    .option-btn {
        background: white;
        border: 1px solid #e0e0e0;
        padding: 10px 18px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.85em;
        color: #333;
        transition: all 0.2s;
    }
    
    .option-btn:hover {
        border-color: #d32f2f;
        background: #fff5f5;
    }
    
    /* Status Badge */
    .status-done {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: #4caf50;
        font-weight: 600;
        margin-bottom: 8px;
        font-size: 0.9em;
    }
    
    /* Responsive */
    @media (max-width: 1024px) {
        .main-cards {
            grid-template-columns: 1fr;
        }
        .card-box {
            border-left: 1px solid #e8e8e8 !important;
            border-radius: 8px !important;
            margin-bottom: 10px;
        }
        .quick-actions-row {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    </style>
""", unsafe_allow_html=True)

# ========================================
# SIDEBAR - API KEY (LEFT SIDE)
# ========================================
with st.sidebar:
    st.markdown("### 🔑 OpenAI API Key")
    st.markdown("Enter your API key to enable AI chat functionality")
    
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
        st.info("ℹ️ API key required for chat")
        st.session_state.api_key_set = False
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Settings")
    user_name = st.text_input("Your Name:", value=st.session_state.user_name)
    st.session_state.user_name = user_name
    
    if st.button("🔄 Reset All", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_view = "home"
        st.session_state.onboarding_step = 0
        st.session_state.experience_level = None
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📚 Resources")
    st.markdown("[📖 Help Center](https://hmarkets.com)")
    st.markdown("[🎓 Education](https://hmarkets.com/learn-to-trade/)")
    st.markdown("[📞 Support](https://hmarkets.com)")
    
    st.markdown("---")
    st.caption("**Hantec Markets**")
    st.caption("Multi-regulated broker")

# ========================================
# TOP NAVIGATION
# ========================================
st.markdown(f"""
    <div class="top-nav">
        <div class="nav-left">
            <div class="hantec-logo">H</div>
            <span class="nav-breadcrumb">Hantec Retail</span>
            <span class="nav-breadcrumb">›</span>
            <span style="color: #333; font-weight: 500; font-size: 0.9em;">Dashboard</span>
        </div>
        <div class="nav-right">
            <span style="font-size: 1.1em; color: #666;">🔍</span>
            <span style="font-size: 1.1em; color: #666;">🔔</span>
            <span class="nav-badge badge-lite">Lite</span>
            <span class="nav-badge badge-pro">Pro</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ========================================
# MAIN CONTENT
# ========================================

if st.session_state.current_view == "home":
    # Welcome Section
    st.markdown(f"""
        <div class="welcome-section">
            <div class="hantec-avatar">
                <span class="avatar-h">H</span>
            </div>
            <h1 class="welcome-title">Welcome to Hantec one, {st.session_state.user_name} 👋</h1>
            <p class="welcome-subtitle">Pick an option below to continue — or ask me anything to get started</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Main Action Cards
    st.markdown("""
        <div class="main-cards">
            <div class="card-box" id="card-trading">
                <div class="card-header">
                    <span class="card-icon">🚀</span>
                    <span class="card-title">Start Live Trading</span>
                </div>
                <div class="card-description">
                    Tell me your goal and account preferences — I'll set up your account to start trading
                </div>
            </div>
            
            <div class="card-box" id="card-fundamentals">
                <div class="card-header">
                    <span class="card-icon">📚</span>
                    <span class="card-title">Master the fundamentals</span>
                </div>
                <div class="card-items">
                    <div class="card-item">
                        <span>📖</span>
                        <span>Try simple examples</span>
                    </div>
                    <div class="card-item">
                        <span>📊</span>
                        <span>Level up your skills</span>
                    </div>
                </div>
            </div>
            
            <div class="card-box" id="card-tour">
                <div class="card-header">
                    <span class="card-icon">💬</span>
                    <span class="card-title">Take a Quick Tour</span>
                </div>
                <div class="card-description">
                    A quick walkthrough of your dashboard, features and charts
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Hidden buttons for card clicks
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Start Live Trading", key="btn1", use_container_width=True):
            st.session_state.current_view = "trading"
            st.session_state.onboarding_step = 1
            st.rerun()
    with col2:
        if st.button("Master Fundamentals", key="btn2", use_container_width=True):
            st.session_state.current_view = "fundamentals"
            st.rerun()
    with col3:
        if st.button("Take a Tour", key="btn3", use_container_width=True):
            st.session_state.current_view = "walkthrough"
            st.rerun()
    
    # Quick Actions
    st.markdown("""
        <div class="quick-actions-row">
            <div class="quick-action-box">
                <span>🎯</span>
                <span>Try demo trading</span>
            </div>
            <div class="quick-action-box">
                <span>📈</span>
                <span>Analyze market</span>
            </div>
            <div class="quick-action-box">
                <span>⚡</span>
                <span>Glossary</span>
            </div>
            <div class="quick-action-box">
                <span>📋</span>
                <span>Make a plan</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Chat Input
    st.markdown('<div class="chat-input-area">', unsafe_allow_html=True)
    if prompt := st.chat_input("Ask me anything...", disabled=not st.session_state.api_key_set):
        st.session_state.current_view = "trading"
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class="page-footer">
            All chats are private & encrypted. Hpulse may make mistakes — verify 
            <a href="#">Key info ↗</a>
        </div>
    """, unsafe_allow_html=True)

# ========================================
# TRADING VIEW - CONVERSATIONAL FLOW
# ========================================
elif st.session_state.current_view == "trading":
    
    # Chat Header
    st.markdown(f"""
        <div class="chat-header">
            <div class="header-left">
                <span>▼</span>
                <span style="font-weight: 600;">Getting started!</span>
                <span class="section-badge">Current</span>
            </div>
            <div class="header-right">
                <span style="font-weight: 500;">Start Live Trading</span>
                <div style="width: 28px; height: 28px; border-radius: 50%; background: #e0e0e0;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Chat Container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Initial greeting
    if st.session_state.onboarding_step == 1 and not st.session_state.messages:
        st.markdown("""
            <div class="message-row">
                <div class="message-avatar avatar-hantec">H</div>
                <div class="message-content">
                    <strong>Awesome, James! Let's get you started 💝</strong><br><br>
                    Before we begin — can you tell me how familiar you are with trading? Pick one below
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1.2, 1.5, 1.5])
        with col1:
            if st.button("I'm completely new", key="new", use_container_width=True):
                st.session_state.experience_level = "new"
                st.session_state.messages.append({"role": "user", "content": "I'm completely new"})
                st.session_state.onboarding_step = 2
                st.rerun()
        with col2:
            if st.button("I have some experience", key="some", use_container_width=True):
                st.session_state.experience_level = "some"
                st.session_state.messages.append({"role": "user", "content": "I have some experience"})
                st.session_state.onboarding_step = 2
                st.rerun()
        with col3:
            if st.button("I'm an experienced trader", key="exp", use_container_width=True):
                st.session_state.experience_level = "experienced"
                st.session_state.messages.append({"role": "user", "content": "I'm an experienced trader"})
                st.session_state.onboarding_step = 2
                st.rerun()
    
    # Display messages
    for msg in st.session_state.messages:
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
    
    # Step 2: Response
    if st.session_state.onboarding_step == 2 and len(st.session_state.messages) == 1:
        st.markdown("""
            <div class="message-row">
                <div class="message-avatar avatar-hantec">H</div>
                <div class="message-content">
                    <strong>Perfect! I'll keep things simple and guide you all the way.</strong><br><br>
                    I'll tailor things based on your experience, so you only see what matters most to you
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Continue", key="cont"):
            st.session_state.messages.append({"role": "assistant", "content": "Perfect! I'll keep things simple and guide you all the way.<br><br>I'll tailor things based on your experience, so you only see what matters most to you"})
            st.session_state.onboarding_step = 3
            st.rerun()
    
    # Step 3: Done + next steps
    if st.session_state.onboarding_step == 3 and len(st.session_state.messages) == 2:
        st.markdown("""
            <div class="message-row">
                <div class="message-avatar avatar-hantec">H</div>
                <div class="message-content">
                    <div class="status-done">
                        <span>✅</span>
                        <span>Done</span>
                    </div>
                    <div>Now tell me what you'd like to do next</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Start live trading right away", key="opt1", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Start live trading right away"})
                st.rerun()
        with col2:
            if st.button("Open a demo account", key="opt2", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Open a demo account and practice"})
                st.rerun()
        with col3:
            if st.button("Try a product demo", key="opt3", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Try a quick product demo"})
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask me anything...", disabled=not st.session_state.api_key_set):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        if st.session_state.api_key_set:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are Hantec One AI. Keep responses under 50 words. Be helpful and friendly."},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                    ],
                    temperature=0.7,
                    max_tokens=100
                )
                answer = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.markdown("""
        <div class="page-footer">
            All chats are private & encrypted. Hpulse may make mistakes — verify 
            <a href="#">Key info ↗</a>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Home"):
        st.session_state.current_view = "home"
        st.rerun()

# Other views...
elif st.session_state.current_view == "fundamentals":
    st.markdown("### 📚 Master the Fundamentals")
    if st.button("← Back"):
        st.session_state.current_view = "home"
        st.rerun()
    st.markdown("Educational content here...")

elif st.session_state.current_view == "walkthrough":
    st.markdown("### 💬 Platform Walkthrough")
    if st.button("← Back"):
        st.session_state.current_view = "home"
        st.rerun()
    st.markdown("Tour content here...")

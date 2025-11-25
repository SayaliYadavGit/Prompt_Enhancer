import streamlit as st
from openai import OpenAI
import time

# ========================================
# PAGE CONFIGURATION
# ========================================
st.set_page_config(
    page_title="Hantec One",
    page_icon="🅷",
    layout="wide",
    initial_sidebar_state="collapsed"
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
# CUSTOM CSS
# ========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
    
    /* Main container */
    .main {
        background-color: #fafafa;
        padding: 0;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Top Navigation */
    .top-nav {
        background: white;
        padding: 12px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #e8e8e8;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .hantec-logo {
        color: #d32f2f;
        font-size: 1.8em;
        font-weight: 700;
    }
    
    /* Chat Container */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 40px 20px;
    }
    
    /* Section Header */
    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px;
        background: white;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.1em;
        font-weight: 600;
    }
    
    .current-badge {
        background: #ffebee;
        color: #d32f2f;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75em;
        font-weight: 600;
    }
    
    /* Chat Messages */
    .chat-message {
        display: flex;
        gap: 15px;
        margin-bottom: 25px;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .message-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.9em;
    }
    
    .avatar-assistant {
        background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
        color: white;
        font-style: italic;
    }
    
    .avatar-user {
        background: #e0e0e0;
    }
    
    .message-content {
        flex: 1;
    }
    
    .message-text {
        color: #333;
        line-height: 1.6;
        font-size: 0.95em;
    }
    
    /* User response buttons */
    .response-options {
        display: flex;
        gap: 10px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    
    .response-btn {
        background: white;
        border: 1px solid #e0e0e0;
        padding: 12px 20px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 0.9em;
    }
    
    .response-btn:hover {
        border-color: #d32f2f;
        background: #fff5f5;
    }
    
    .response-btn.selected {
        background: #f5f5f5;
        border-color: #999;
    }
    
    /* Status indicator */
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #666;
        font-size: 0.9em;
        margin-bottom: 15px;
    }
    
    .status-check {
        color: #4caf50;
        font-size: 1.2em;
    }
    
    /* Action chips */
    .action-chips {
        display: flex;
        gap: 10px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    
    .action-chip {
        background: white;
        border: 1px solid #e0e0e0;
        padding: 10px 18px;
        border-radius: 20px;
        font-size: 0.85em;
        cursor: pointer;
        transition: all 0.2s;
        white-space: nowrap;
    }
    
    .action-chip:hover {
        border-color: #d32f2f;
        background: #fff5f5;
        transform: translateY(-2px);
    }
    
    /* Chat input area */
    .chat-input-wrapper {
        position: sticky;
        bottom: 0;
        background: #fafafa;
        padding: 20px 0;
        border-top: 1px solid #e8e8e8;
    }
    
    .stChatInput {
        max-width: 900px;
        margin: 0 auto;
    }
    
    /* Footer */
    .chat-footer {
        text-align: center;
        color: #999;
        font-size: 0.8em;
        padding: 15px;
    }
    
    /* Welcome cards */
    .welcome-container {
        text-align: center;
        padding: 60px 20px 40px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .hantec-avatar {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
        border-radius: 50%;
        margin: 0 auto 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    
    .avatar-text {
        color: white;
        font-size: 2em;
        font-weight: 700;
        font-style: italic;
    }
    
    .welcome-title {
        font-size: 2em;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 10px;
    }
    
    .welcome-subtitle {
        color: #666;
        font-size: 1.05em;
        margin-bottom: 50px;
    }
    
    .cards-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        max-width: 1200px;
        margin: 0 auto 40px;
        padding: 0 20px;
    }
    
    .action-card {
        background: white;
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        min-height: 200px;
        display: flex;
        flex-direction: column;
    }
    
    .action-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }
    
    .action-card.primary {
        background: linear-gradient(135deg, #8B0000 0%, #a01515 100%);
        color: white;
    }
    
    .card-icon {
        font-size: 1.5em;
        margin-bottom: 15px;
    }
    
    .card-title {
        font-size: 1.3em;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .card-description {
        font-size: 0.95em;
        opacity: 0.9;
        line-height: 1.5;
        flex-grow: 1;
    }
    
    .card-items {
        margin-top: 15px;
    }
    
    .card-item {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        font-size: 0.9em;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .cards-container {
            grid-template-columns: 1fr;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ========================================
# SIDEBAR - API KEY
# ========================================
with st.sidebar:
    st.markdown("### 🔑 OpenAI API Key")
    
    api_key = st.text_input(
        "Enter your API key:",
        type="password",
        placeholder="sk-proj-...",
        help="Required for AI chat functionality"
    )
    
    if api_key:
        if api_key.startswith('sk-'):
            st.success("✅ Active")
            st.session_state.api_key_set = True
            try:
                client = OpenAI(api_key=api_key)
            except:
                st.error("❌ Invalid")
                st.session_state.api_key_set = False
        else:
            st.warning("⚠️ Invalid format")
            st.session_state.api_key_set = False
    else:
        st.info("ℹ️ Enter key to chat")
        st.session_state.api_key_set = False
    
    st.markdown("---")
    
    user_name = st.text_input("Your Name:", value=st.session_state.user_name)
    st.session_state.user_name = user_name
    
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_view = "home"
        st.session_state.onboarding_step = 0
        st.session_state.experience_level = None
        st.rerun()
    
    st.markdown("---")
    st.caption("**Hantec One**")
    st.caption("[Visit hmarkets.com](https://hmarkets.com)")

# ========================================
# TOP NAVIGATION
# ========================================
st.markdown("""
    <div class="top-nav">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div class="hantec-logo">H</div>
            <span style="color: #999;">Hantec Retail</span>
            <span style="color: #999;">›</span>
            <span style="color: #333; font-weight: 500;">Dashboard</span>
        </div>
        <div style="display: flex; gap: 15px; align-items: center;">
            <span>🔍</span>
            <span>🔔</span>
            <span style="padding: 4px 12px; background: #f0f0f0; border-radius: 6px; font-size: 0.85em;">Lite</span>
            <span style="padding: 4px 12px; background: #8B0000; color: white; border-radius: 6px; font-size: 0.85em;">Pro</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ========================================
# MAIN CONTENT
# ========================================

if st.session_state.current_view == "home":
    # Home dashboard
    st.markdown(f"""
        <div class="welcome-container">
            <div class="hantec-avatar">
                <span class="avatar-text">H</span>
            </div>
            <h1 class="welcome-title">Welcome to Hantec one, {st.session_state.user_name} 👋</h1>
            <p class="welcome-subtitle">Pick an option below to continue — or ask me anything to get started</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Action Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Start Live Trading\n\nTell me your goal and account preferences — I'll set up your account to start trading", key="card1", use_container_width=True):
            st.session_state.current_view = "trading"
            st.session_state.messages = []
            st.session_state.onboarding_step = 1
            st.rerun()
    
    with col2:
        if st.button("📚 Master the fundamentals\n\n📖 Try simple examples\n📊 Level up your skills", key="card2", use_container_width=True):
            st.session_state.current_view = "fundamentals"
            st.rerun()
    
    with col3:
        if st.button("💬 Take a Quick Tour\n\nA quick walkthrough of your dashboard, features and charts", key="card3", use_container_width=True):
            st.session_state.current_view = "walkthrough"
            st.rerun()
    
    # Quick actions
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("🎯 Try demo trading", use_container_width=True)
    with col2:
        st.button("📈 Analyze market", use_container_width=True)
    with col3:
        st.button("⚡ Glossary", use_container_width=True)
    with col4:
        st.button("📋 Make a plan", use_container_width=True)
    
    # Chat input
    st.markdown("<br><br>", unsafe_allow_html=True)
    if prompt := st.chat_input("Ask me anything...", disabled=not st.session_state.api_key_set):
        st.session_state.current_view = "trading"
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()
    
    st.markdown("""
        <div class="chat-footer">
            All chats are private & encrypted. Hpulse may make mistakes — verify 
            <a href="#" style="color: #d32f2f;">Key info ↗</a>
        </div>
    """, unsafe_allow_html=True)

# ========================================
# START LIVE TRADING - ONBOARDING FLOW
# ========================================
elif st.session_state.current_view == "trading":
    
    # Section header
    st.markdown("""
        <div class="section-header">
            <div class="section-title">
                <span>▼</span>
                <span>Getting started!</span>
                <span class="current-badge">Current</span>
            </div>
            <div style="display: flex; align-items: center; gap: 15px;">
                <span style="font-weight: 500;">Start Live Trading</span>
                <img src="https://ui-avatars.com/api/?name=J&background=e0e0e0&color=666&size=32&rounded=true" style="border-radius: 50%;" />
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Initial onboarding flow
    if st.session_state.onboarding_step == 1 and not st.session_state.messages:
        # Step 1: Welcome
        st.markdown("""
            <div class="chat-message">
                <div class="message-avatar avatar-assistant">H</div>
                <div class="message-content">
                    <div class="message-text">
                        <strong>Awesome, James! Let's get you started 💝</strong><br><br>
                        Before we begin — can you tell me how familiar you are with trading? Pick one below
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Experience level options
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("I'm completely new", key="exp_new", use_container_width=True):
                st.session_state.experience_level = "new"
                st.session_state.messages.append({
                    "role": "user",
                    "content": "I'm completely new",
                    "avatar": "user"
                })
                st.session_state.onboarding_step = 2
                st.rerun()
        
        with col2:
            if st.button("I have some experience", key="exp_some", use_container_width=True):
                st.session_state.experience_level = "some"
                st.session_state.messages.append({
                    "role": "user",
                    "content": "I have some experience"
                })
                st.session_state.onboarding_step = 2
                st.rerun()
        
        with col3:
            if st.button("I'm an experienced trader", key="exp_pro", use_container_width=True):
                st.session_state.experience_level = "experienced"
                st.session_state.messages.append({
                    "role": "user",
                    "content": "I'm an experienced trader"
                })
                st.session_state.onboarding_step = 2
                st.rerun()
    
    # Display conversation history
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="chat-message" style="justify-content: flex-end;">
                    <div class="message-content" style="text-align: right;">
                        <div class="message-text" style="background: #f5f5f5; display: inline-block; padding: 12px 18px; border-radius: 18px;">
                            {msg["content"]}
                        </div>
                    </div>
                    <div class="message-avatar avatar-user">
                        <img src="https://ui-avatars.com/api/?name=J&background=e0e0e0&color=666&size=36&rounded=true" style="border-radius: 50%; width: 36px; height: 36px;" />
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message">
                    <div class="message-avatar avatar-assistant">H</div>
                    <div class="message-content">
                        <div class="message-text">{msg["content"]}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Step 2: Personalized response
    if st.session_state.onboarding_step == 2 and len(st.session_state.messages) == 1:
        st.markdown("""
            <div class="chat-message">
                <div class="message-avatar avatar-assistant">H</div>
                <div class="message-content">
                    <div class="message-text">
                        <strong>Perfect! I'll keep things simple and guide you all the way.</strong><br><br>
                        I'll tailor things based on your experience, so you only see what matters most to you
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Auto-progress after 2 seconds
        time.sleep(2)
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Perfect! I'll keep things simple and guide you all the way.<br><br>I'll tailor things based on your experience, so you only see what matters most to you"
        })
        st.session_state.onboarding_step = 3
        st.rerun()
    
    # Step 3: Done + Next steps
    if st.session_state.onboarding_step == 3 and len(st.session_state.messages) == 2:
        st.markdown("""
            <div class="chat-message">
                <div class="message-avatar avatar-assistant">H</div>
                <div class="message-content">
                    <div class="status-indicator">
                        <span class="status-check">✅</span>
                        <strong>Done</strong>
                    </div>
                    <div class="message-text">
                        Now tell me what you'd like to do next
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Action options
        st.markdown("""
            <div class="action-chips">
                <div class="action-chip">Start live trading right away</div>
                <div class="action-chip">Open a demo account and practice</div>
                <div class="action-chip">Try a quick product demo</div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Start live trading right away", key="opt1", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Start live trading right away"})
                st.session_state.onboarding_step = 4
                st.rerun()
        with col2:
            if st.button("Open a demo account and practice", key="opt2", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Open a demo account and practice"})
                st.session_state.onboarding_step = 4
                st.rerun()
        with col3:
            if st.button("Try a quick product demo", key="opt3", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Try a quick product demo"})
                st.session_state.onboarding_step = 4
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input for free-form questions
    if prompt := st.chat_input("Ask me anything...", disabled=not st.session_state.api_key_set):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        if st.session_state.api_key_set:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": """You are Hantec One AI assistant. Keep responses SHORT (2-3 sentences, max 50 words). Be friendly, helpful, and guide users through trading setup. Never give buy/sell signals."""},
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
        <div class="chat-footer">
            All chats are private & encrypted. Hpulse may make mistakes — verify 
            <a href="#" style="color: #d32f2f;">Key info ↗</a>
        </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_view = "home"
        st.rerun()

# ========================================
# MASTER FUNDAMENTALS
# ========================================
elif st.session_state.current_view == "fundamentals":
    st.markdown("### 📚 Master the Fundamentals")
    
    if st.button("← Back to Home"):
        st.session_state.current_view = "home"
        st.rerun()
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📖 Getting Started", "📊 Technical Analysis", "💰 Risk Management"])
    
    with tab1:
        st.markdown("""
        ## Getting Started with Trading
        
        ### What is Forex Trading?
        Forex trading involves buying and selling currency pairs to profit from exchange rate changes.
        
        **Key Concepts:**
        - **Currency Pairs**: EUR/USD, GBP/USD, USD/JPY
        - **Pips**: Smallest price movement (0.0001)
        - **Lots**: Standard (100,000), Mini (10,000), Micro (1,000)
        - **Leverage**: Trade larger positions with less capital
        """)
    
    with tab2:
        st.markdown("""
        ## Technical Analysis
        
        Learn to read charts, identify trends, and use indicators effectively.
        """)
    
    with tab3:
        st.markdown("""
        ## Risk Management
        
        Master the golden rules of trading risk management.
        """)

# ========================================
# WALKTHROUGH
# ========================================
elif st.session_state.current_view == "walkthrough":
    st.markdown("### 💬 Platform Walkthrough")
    
    if st.button("← Back to Home"):
        st.session_state.current_view = "home"
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    ## Quick Platform Tour
    
    Learn about your dashboard, features, and trading tools.
    """)

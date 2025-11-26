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
    
    /* Top Navigation - Hide it */
    .top-nav {
        display: none;
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
    
    /* Main Cards - Fixed grid */
    .main-cards-wrapper {
        max-width: 1400px;
        margin: 0 auto 50px;
        padding: 0 20px;
    }
    
    /* Remove gap styling since we're using columns */
    div[data-testid="column"] {
        padding: 0 !important;
    }
    
    div[data-testid="column"]:first-child .card-box {
        border-top-left-radius: 8px;
        border-bottom-left-radius: 8px;
    }
    
    div[data-testid="column"]:last-child .card-box {
        border-top-right-radius: 8px;
        border-bottom-right-radius: 8px;
    }
    
    div[data-testid="column"]:not(:first-child) .card-box {
        border-left: none;
    }
    
    .card-box {
        background: white;
        border: 1px solid #e8e8e8;
        padding: 28px;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        transition: background 0.2s ease;
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
    
    /* Hide default streamlit buttons - better selector */
    div[data-testid="column"] button {
        opacity: 0;
        position: absolute;
        pointer-events: none;
        height: 0;
        width: 0;
    }
    
    /* Make cards clickable */
    .card-box {
        cursor: pointer;
        position: relative;
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

# ========================================
# TOP NAVIGATION
# ========================================
st.markdown("""
    <div class="top-nav">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div class="hantec-logo">H</div>
            <span style="color: #999; font-size: 0.9em;">Hantec Retail</span>
            <span style="color: #999;">›</span>
            <span style="color: #333; font-weight: 500; font-size: 0.9em;">Dashboard</span>
        </div>
        <div style="display: flex; align-items: center; gap: 15px;">
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
    st.markdown("""
        <div class="welcome-section">
            <div class="hantec-avatar">
                <span class="avatar-h">H</span>
            </div>
            <h1 class="welcome-title">Welcome to Hantec One</h1>
            <p class="welcome-subtitle">Pick an option below to continue - or ask me anything to get started</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Main Action Cards - Match Figma Design
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🚀 Start Live Trading")
        st.markdown("Tell me your goal and account preferences — I'll set up your account to start trading")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("→", key="btn1"):
            st.session_state.current_view = "trading"
            st.session_state.onboarding_step = 1
            st.rerun()
    
    with col2:
        st.markdown("### 📚 Master the fundamentals")
        st.markdown("📖 Try simple examples")
        st.markdown("📊 Level up your skills")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("→", key="btn2"):
            st.session_state.current_view = "cfds"
            st.rerun()
    
    with col3:
        st.markdown("### Take a Quick Tour")
        st.markdown("A quick walkthrough of your dashboard, features and charts")
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("→", key="btn3"):
            st.session_state.current_view = "tour"
            st.rerun()
    
    # Chat Input
    st.markdown('<div class="chat-input-area">', unsafe_allow_html=True)
    
    if not st.session_state.api_key_set:
        st.info("Enter your OpenAI API key in the sidebar to start chatting")
    
    if prompt := st.chat_input("Ask me anything...", disabled=not st.session_state.api_key_set):
        # Add user message
        st.session_state.current_view = "trading"
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get AI response
        if st.session_state.api_key_set:
            try:
                with st.spinner("Thinking..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": """You are Hantec One AI trading mentor. Follow these strict guidelines:

**Brand Voice:**
- Knowledgeable but humble ("I am here to help you learn")
- Empowering and patient
- Never condescending
- Motivational and celebratory of milestones

**Response Style:**
- SHORT answers (2-3 sentences, max 60 words)
- Use bullet points for lists
- Be precise and to-the-point
- Use **bold** for emphasis

**What You CAN Help With:**
- Trading education and concepts
- Platform navigation
- Onboarding guidance
- CFD basics
- Risk management education

**What You MUST NEVER Do:**
- Give specific buy/sell signals
- Guarantee returns
- Provide financial advice
- Share personal information

**Compliance - ALWAYS Include:**
- Risk disclaimers on trading questions
- "For educational purposes only" on investment topics
- "Not financial advice" disclaimer

**Response Format:**
Keep it conversational but structured. Use emojis sparingly.

**If Unclear:**
Say: "I did not understand. Can we try this again?" and offer multiple choice options.

**Escalation Triggers - Redirect to support if:**
- Account access issues
- Fund withdrawal problems
- Unauthorized trades mentioned
- Complex compliance questions

Example Good Response:
"Leverage lets you control larger positions with less capital. With 1:100 leverage, $100 controls $10,000. Important: It multiplies both gains AND losses. Start with lower leverage (1:10) while learning. For educational purposes only."},
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
    
    # Footer
    st.markdown("""
        <div class="page-footer">
            All chats are private & encrypted. Hpulse may make mistakes - verify 
            <a href="#">Key info</a>
        </div>
    """, unsafe_allow_html=True)

# ========================================
# TRADING VIEW - CONVERSATIONAL FLOW
# ========================================
elif st.session_state.current_view == "trading":
    
    # Chat Header
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
    
    # Chat Container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Initial greeting - Updated per spec
    if st.session_state.onboarding_step == 1 and not st.session_state.messages:
        st.markdown("""
            <div class="message-row">
                <div class="message-avatar avatar-hantec">H</div>
                <div class="message-content">
                    <strong>Hi, I am your trading mentor. Lets start live trading!</strong><br><br>
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
    
    # Display all messages
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
    
    # Step 2: Response - Updated per spec
    if st.session_state.onboarding_step == 2 and len(st.session_state.messages) == 1:
        st.markdown("""
            <div class="message-row">
                <div class="message-avatar avatar-hantec">H</div>
                <div class="message-content">
                    <strong>Perfect! I will guide you all the way.</strong><br><br>
                    I will tailor everything based on your experience level, so you only see what matters most to you.<br><br>
                    Let us get you set up for trading success!
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Continue ->", key="cont"):
            st.session_state.messages.append({"role": "assistant", "content": "Perfect! I'll keep things simple and guide you all the way.<br><br>I'll tailor things based on your experience, so you only see what matters most to you"})
            st.session_state.onboarding_step = 3
            st.rerun()
    
    # Step 3: Done + next steps
    elif st.session_state.onboarding_step == 3 and len(st.session_state.messages) == 2:
        st.markdown("""
            <div class="message-row">
                <div class="message-avatar avatar-hantec">H</div>
                <div class="message-content">
                    <div class="status-done">
                        <span>DONE</span>
                        <span>Done</span>
                    </div>
                    <div>Now tell me what you would like to do next</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Start live trading", key="opt1", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Start live trading right away"})
                st.session_state.onboarding_step = 4
                st.rerun()
        with col2:
            if st.button("Demo account", key="opt2", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Open a demo account and practice"})
                st.session_state.onboarding_step = 4
                st.rerun()
        with col3:
            if st.button("Product demo", key="opt3", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Try a quick product demo"})
                st.session_state.onboarding_step = 4
                st.rerun()
    
    # Step 4+: Free chat enabled
    elif st.session_state.onboarding_step >= 4 or len(st.session_state.messages) > 2:
        st.session_state.onboarding_step = 4  # Enable free chat
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input - Always available when API key is set
    if prompt := st.chat_input("Ask me anything...", disabled=not st.session_state.api_key_set):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        if st.session_state.api_key_set:
            try:
                with st.spinner("Thinking..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": """You are Hantec One AI trading assistant. 

Keep responses SHORT (2-3 sentences, max 60 words).
Help with trading, CFDs, platform features, account setup.
Be friendly and professional. Never give buy/sell signals."""},
                            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-6:]]
                        ],
                        temperature=0.7,
                        max_tokens=150
                    )
                    answer = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.session_state.onboarding_step = 4  # Enable free chat
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        st.rerun()
    
    st.markdown("""
        <div class="page-footer">
            All chats are private & encrypted. Hpulse may make mistakes - verify 
            <a href="#">Key info ↗</a>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Home"):
        st.session_state.current_view = "home"
        st.session_state.messages = []
        st.session_state.onboarding_step = 0
        st.rerun()

# ========================================
# NEW TO TRADING - LEARNING PATH
# ========================================
elif st.session_state.current_view == "learning":
    st.markdown("### New to Trading? Let us Build Your Learning Plan")
    
    if st.button("← Back to Home"):
        st.session_state.current_view = "home"
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    ## Hey, do not worry - I am here to assist you!
    
    Let us get to know each other so I can create a personalized learning plan.
    """)
    
    # Quick questionnaire
    col1, col2 = st.columns(2)
    
    with col1:
        years_exp = st.selectbox(
            "Years of trading experience:",
            ["None - Complete beginner", "Less than 1 year", "1-3 years", "3-5 years", "5+ years"]
        )
        
        age_range = st.selectbox(
            "Your age range:",
            ["18-25", "26-35", "36-45", "46-55", "56+"]
        )
    
    with col2:
        risk_tolerance = st.selectbox(
            "Risk tolerance:",
            ["Conservative - Preserve capital", "Moderate - Balanced approach", "Aggressive - Maximum growth"]
        )
        
        learning_goal = st.selectbox(
            "Primary learning goal:",
            ["Understand basics", "Learn strategies", "Master technical analysis", "Risk management"]
        )
    
            if st.button("Create My Learning Plan", type="primary", use_container_width=True):
        st.success("Learning plan created!")
        
        st.markdown("---")
        st.markdown("## Your Personalized Curriculum")
        
        st.markdown("""
        Based on your profile, here is your learning journey:
        
        ### Week 1: Trading Fundamentals
        - What is CFD trading?
        - Understanding leverage
        - Key trading terminology
        - Market types (Forex, Indices, Commodities)
        
        ### Week 2: Platform Basics
        - Navigate Hantec dashboard
        - Place your first demo trade
        - Understanding order types
        - Reading charts basics
        
        ### Week 3: Risk Management
        - Position sizing
        - Stop-loss strategies
        - Risk/reward ratios
        - Portfolio management
        
        ### Week 4: Technical Analysis Intro
        - Support & resistance
        - Trend identification
        - Key indicators (MA, RSI, MACD)
        
        **Important:** Practice on demo account before live trading. All trading involves risk.
        
        [Start Week 1] [Open Demo Account]
        """)

# ========================================
# LEARN CFDs VIEW (Renamed from previous)
# ========================================
elif st.session_state.current_view == "cfds":
    st.markdown("### 📚 Learn CFDs")
    
    if st.button("← Back to Home"):
        st.session_state.current_view = "home"
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    ## Master the Fundamentals
    
    ### What are CFDs?
    Contracts for Difference (CFDs) allow you to trade on price movements without owning the underlying asset.
    
    ### Key Concepts
    - **Leverage trading**: Control larger positions with smaller capital
    - **Long and short positions**: Profit from rising or falling markets
    - **Margin requirements**: Understand deposit requirements
    - **Risk management**: Essential strategies for success
    
    ### Popular CFD Instruments
    - Forex pairs (EUR/USD, GBP/USD)
    - Indices (S&P 500, FTSE 100)
    - Commodities (Gold, Oil)
    - Cryptocurrencies (Bitcoin, Ethereum)
    """)

# ========================================
# TAKE A TOUR VIEW
# ========================================
elif st.session_state.current_view == "tour":
    st.markdown("### 💬 Take a Quick Tour")
    
    if st.button("← Back to Home"):
        st.session_state.current_view = "home"
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    ## Platform Walkthrough
    
    Learn about your dashboard, features, and trading tools.
    
    ### Dashboard Overview
    - Account balance and equity
    - Open positions
    - Market watchlist
    - Trading history
    
    ### Trading Platform Features
    - Multiple chart types and timeframes
    - 50+ technical indicators
    - One-click trading
    - Advanced order types (stop-loss, take-profit)
    
    ### Getting Started
    1. Fund your account
    2. Choose your instrument
    3. Analyze the market
    4. Place your trade
    5. Monitor and manage positions
    """)

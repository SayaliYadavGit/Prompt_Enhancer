import streamlit as st
from openai import OpenAI

# ========================================
# PAGE CONFIGURATION
# ========================================
st.set_page_config(
    page_title="Hantec Markets AI Trading Mentor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# CUSTOM CSS - HANTEC MARKETS BRANDING
# Colors from hmarkets.com: Dark blue, orange accents, professional
# ========================================
st.markdown("""
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main header with Hantec branding */
    .main-header {
        background: linear-gradient(135deg, #0a1628 0%, #1a2f4d 100%);
        padding: 30px 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        border-bottom: 3px solid #ff6b35;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-bottom: 10px;
    }
    
    .logo-text {
        color: white;
        font-size: 2.8em;
        font-weight: 700;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .logo-markets {
        color: #ff6b35;
        font-weight: 600;
    }
    
    .tagline {
        color: #b8c5d6;
        font-size: 1.2em;
        margin-top: 8px;
        font-weight: 400;
    }
    
    .trust-badge {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px 20px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 15px;
        color: #fff;
        font-size: 0.9em;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 15px;
        animation: fadeIn 0.4s ease-out;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .user-message {
        background: linear-gradient(135deg, #e8f4f8 0%, #d4e9f2 100%);
        border-left: 4px solid #0a1628;
        margin-left: 40px;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-left: 4px solid #ff6b35;
        margin-right: 40px;
    }
    
    .message-role {
        font-weight: 600;
        color: #0a1628;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .message-content {
        color: #2c3e50;
        line-height: 1.7;
        font-size: 1.02em;
    }
    
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(15px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    /* Buttons - Hantec style */
    .stButton>button {
        background: linear-gradient(135deg, #ff6b35 0%, #ff8c5a 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 1em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff8c5a 0%, #ff6b35 100%);
        box-shadow: 0 6px 16px rgba(255, 107, 53, 0.4);
        transform: translateY(-2px);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Input styling */
    .stChatInput {
        border: 2px solid #e0e6ed;
        border-radius: 8px;
    }
    
    /* Info boxes */
    .info-card {
        background: linear-gradient(135deg, #fff5f2 0%, #ffe8df 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ff6b35;
        margin: 10px 0;
    }
    
    .stats-container {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ========================================
# HEADER WITH HANTEC MARKETS BRANDING
# ========================================
st.markdown("""
    <div class="main-header">
        <div class="logo-container">
            <h1 class="logo-text">HANTEC <span class="logo-markets">MARKETS</span></h1>
        </div>
        <p class="tagline">AI Trading Mentor | Trade Better. Learn Smarter.</p>
        <div class="trust-badge">
            🌍 Trusted by 200,000+ Traders Worldwide | 6 Global Regulations
        </div>
    </div>
""", unsafe_allow_html=True)

# ========================================
# SESSION STATE INITIALIZATION
# ========================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False

# ========================================
# SIDEBAR - API KEY & INFO
# ========================================
with st.sidebar:
    st.markdown("### 🔑 API Configuration")
    
    api_key = st.text_input(
        "OpenAI API Key:",
        type="password",
        help="Your API key enables the AI mentor",
        placeholder="sk-proj-..."
    )
    
    # Validate API key
    if api_key:
        if api_key.startswith('sk-'):
            st.success("✅ API Key Active")
            st.session_state.api_key_set = True
            try:
                client = OpenAI(api_key=api_key)
            except Exception as e:
                st.error("❌ Invalid API Key")
                st.session_state.api_key_set = False
        else:
            st.warning("⚠️ Key should start with 'sk-'")
            st.session_state.api_key_set = False
    else:
        st.info("ℹ️ Enter your API key to activate mentor")
        st.session_state.api_key_set = False
    
    st.markdown("---")
    
    # Trading Topics
    st.markdown("### 📚 What You Can Learn")
    st.markdown("""
    **Forex & CFDs:**
    - Currency pair basics
    - Spread & pip explanation
    - Leverage understanding
    
    **Risk Management:**
    - Position sizing rules
    - Stop-loss strategies
    - Portfolio protection
    
    **Technical Analysis:**
    - Chart patterns
    - Indicators & signals
    - Trend identification
    
    **Trading Psychology:**
    - Emotional control
    - Discipline building
    - Common mistakes
    """)
    
    st.markdown("---")
    
    # Hantec Features
    st.markdown("### 🎯 Why Hantec Markets?")
    st.markdown("""
    ✅ **0.1 pips** starting spreads  
    ✅ **500:1** leverage available  
    ✅ **2000+** instruments  
    ✅ **5 min** withdrawal processing  
    ✅ **6** global regulations  
    """)
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("💡 Examples", use_container_width=True):
            st.session_state.show_examples = not st.session_state.get("show_examples", False)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
        <div style='text-align: center; font-size: 0.85em; color: #666;'>
            <p><strong>Hantec Markets</strong></p>
            <p>Multi-regulated CFD broker</p>
            <p style='margin-top: 10px;'>
                <a href='https://hmarkets.com' target='_blank' style='color: #ff6b35; text-decoration: none;'>
                    Visit hmarkets.com →
                </a>
            </p>
        </div>
    """, unsafe_allow_html=True)

# ========================================
# EXAMPLE QUESTIONS
# ========================================
if st.session_state.get("show_examples", False):
    st.markdown("### 💡 Example Questions")
    
    examples = [
        ("🎯 Beginner", "What is forex trading and how does it work?"),
        ("📊 Analysis", "How do I read candlestick charts?"),
        ("🛡️ Risk", "What's the best position size for beginners?"),
        ("📈 Strategy", "Explain support and resistance levels"),
        ("💰 Trading", "What are stop-loss and take-profit orders?"),
    ]
    
    for category, question in examples:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.caption(category)
        with col2:
            if st.button(question, key=question, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": question})
                st.session_state.show_examples = False
                st.rerun()

# ========================================
# DISPLAY CHAT HISTORY
# ========================================
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-role">👤 You</div>
                <div class="message-content">{message["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-message assistant-message">
                <div class="message-role">🤖 Hantec Trading Mentor</div>
                <div class="message-content">{message["content"]}</div>
            </div>
        """, unsafe_allow_html=True)

# ========================================
# CHAT INPUT
# ========================================
user_question = st.chat_input(
    "Ask your trading question here... (e.g., 'What is forex trading?')",
    disabled=not st.session_state.api_key_set
)

# ========================================
# PROCESS USER QUESTION
# ========================================
if user_question:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    # Display user message
    st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-role">👤 You</div>
            <div class="message-content">{user_question}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Generate response
    if st.session_state.api_key_set:
        with st.spinner("🤔 Your mentor is analyzing..."):
            try:
                # System prompt - Hantec Markets personality
                system_prompt = """You are the AI Trading Mentor for Hantec Markets - a professional, multi-regulated CFD and forex broker trusted by 200,000+ traders worldwide.

**Your Mission:**
Educate traders with clear, practical guidance while representing Hantec Markets' values of trust, excellence, and trader success.

**Communication Style:**
- SHORT & PRECISE: 3-5 sentences max (50-80 words total)
- Use simple language - explain jargon when necessary
- Be encouraging and supportive
- Break complex topics into steps
- Provide actionable insights

**Your Expertise:**
- Forex trading (currency pairs, spreads, leverage)
- CFD trading (indices, commodities, metals)
- Technical analysis (charts, indicators, patterns)
- Risk management (stop-loss, position sizing)
- Trading psychology (discipline, emotions)
- Platform features (MetaTrader, execution)

**Hantec Markets Context (mention when relevant):**
- 0.1 pips starting spreads
- 500:1 leverage available
- 2000+ instruments
- 6 global regulations
- 5-minute withdrawals
- Negative balance protection

**Critical Rules:**
1. NEVER give specific trade signals (no "Buy EUR/USD now")
2. NEVER predict market movements ("EUR will rise")
3. ALWAYS emphasize risk management
4. Be educational, not advisory
5. Remind: trading involves substantial risk

**Response Format:**
- Direct answer first (1-2 sentences)
- Supporting explanation (1-2 sentences)
- Practical tip or next step (1 sentence)

Remember: You teach concepts and build trader knowledge. You don't give financial advice."""

                # Call OpenAI API
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *[{"role": m["role"], "content": m["content"]} 
                          for m in st.session_state.messages[-6:]],  # Last 6 messages
                    ],
                    temperature=0.7,
                    max_tokens=150
                )
                
                # Extract response
                assistant_message = response.choices[0].message.content
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                # Display response
                st.markdown(f"""
                    <div class="chat-message assistant-message">
                        <div class="message-role">🤖 Hantec Trading Mentor</div>
                        <div class="message-content">{assistant_message}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Usage stats
                with st.expander("📊 Response Analytics"):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Model", "GPT-4o-mini")
                    with col2:
                        st.metric("Tokens", response.usage.total_tokens)
                    with col3:
                        cost = response.usage.total_tokens * 0.0000015
                        st.metric("Cost", f"${cost:.6f}")
                    with col4:
                        words = len(assistant_message.split())
                        st.metric("Words", words)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Check your API key and ensure you have OpenAI credits available.")
    
    st.rerun()

# ========================================
# FOOTER - DISCLAIMERS & LINKS
# ========================================
st.markdown("---")
st.markdown("""
    <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 30px;'>
        <div style='text-align: center;'>
            <h4 style='color: #0a1628; margin-bottom: 15px;'>⚠️ Important Disclaimer</h4>
            <p style='color: #666; font-size: 0.95em; line-height: 1.6;'>
                This AI mentor provides <strong>educational content only</strong> and does not constitute 
                financial or investment advice. CFD and forex trading carries substantial risk of loss. 
                You should carefully consider whether trading is suitable for you based on your financial 
                situation. Past performance is not indicative of future results.
            </p>
            <p style='color: #666; font-size: 0.9em; margin-top: 15px;'>
                <strong>Hantec Markets</strong> is a multi-regulated broker with 6 global regulations. 
                All client funds are held in segregated accounts with tier-1 banks.
            </p>
            <div style='margin-top: 20px;'>
                <a href='https://hmarkets.com' target='_blank' 
                   style='color: #ff6b35; text-decoration: none; font-weight: 600; margin: 0 15px;'>
                    🌐 Visit hmarkets.com
                </a>
                <a href='https://hmarkets.com/live-account-pre-registration/' target='_blank' 
                   style='color: #ff6b35; text-decoration: none; font-weight: 600; margin: 0 15px;'>
                    📈 Open Trading Account
                </a>
                <a href='https://hmarkets.com/learn-to-trade/learning-hub/' target='_blank' 
                   style='color: #ff6b35; text-decoration: none; font-weight: 600; margin: 0 15px;'>
                    📚 Education Centre
                </a>
            </div>
            <p style='color: #999; font-size: 0.85em; margin-top: 20px;'>
                Powered by OpenAI GPT-4o-mini | Built for Hantec Markets traders
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

import streamlit as st
from openai import OpenAI

# ========================================
# PAGE CONFIGURATION
# ========================================
st.set_page_config(
    page_title="Hantec Markets Trading Mentor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# CUSTOM CSS FOR BRANDING
# ========================================
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .logo-text {
        color: white;
        font-size: 2.5em;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .tagline {
        color: #e0e0e0;
        font-size: 1.1em;
        margin-top: 5px;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        animation: fadeIn 0.5s;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #1e3c72;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stButton>button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 30px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ========================================
# HEADER WITH LOGO
# ========================================
st.markdown("""
    <div class="main-header">
        <h1 class="logo-text">📈 HANTEC MARKETS</h1>
        <p class="tagline">Your AI Trading Mentor - Learn, Trade, Succeed</p>
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
    st.header("🔑 API Configuration")
    
    api_key = st.text_input(
        "OpenAI API Key:",
        type="password",
        help="Enter your OpenAI API key to activate the mentor",
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
        st.info("ℹ️ Enter your API key to begin")
        st.session_state.api_key_set = False
    
    st.markdown("---")
    
    # Trading Topics
    st.header("📚 Trading Topics")
    st.markdown("""
    **What you can ask:**
    - Forex trading basics
    - Risk management strategies
    - Technical analysis
    - Chart patterns
    - Trading psychology
    - Market fundamentals
    - Order types & execution
    - Portfolio management
    """)
    
    st.markdown("---")
    
    # Quick Actions
    st.header("⚡ Quick Actions")
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("💡 Example Questions"):
        st.session_state.show_examples = not st.session_state.get("show_examples", False)
    
    st.markdown("---")
    
    # About
    st.header("ℹ️ About")
    st.caption("""
    **Hantec Markets Trading Mentor**
    
    AI-powered assistant providing:
    - Clear, concise trading guidance
    - Step-by-step learning
    - Beginner-friendly explanations
    
    *Responses are educational only. 
    Not financial advice.*
    """)

# ========================================
# EXAMPLE QUESTIONS (Optional Display)
# ========================================
if st.session_state.get("show_examples", False):
    st.info("💡 **Example Questions:**")
    examples = [
        "What is forex trading?",
        "How do I manage risk in trading?",
        "Explain support and resistance",
        "What are stop-loss orders?",
        "How to read candlestick charts?"
    ]
    for example in examples:
        if st.button(f"📌 {example}", key=example):
            st.session_state.messages.append({"role": "user", "content": example})
            st.session_state.show_examples = False
            st.rerun()

# ========================================
# MAIN CHAT INTERFACE
# ========================================

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong><br>{message["content"]}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 Trading Mentor:</strong><br>{message["content"]}
            </div>
        """, unsafe_allow_html=True)

# Chat input
user_question = st.chat_input(
    "Ask your trading question here...",
    disabled=not st.session_state.api_key_set
)

# ========================================
# PROCESS USER QUESTION
# ========================================
if user_question:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    # Display user message immediately
    st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You:</strong><br>{user_question}
        </div>
    """, unsafe_allow_html=True)
    
    # Generate AI response
    if st.session_state.api_key_set:
        with st.spinner("🤔 Mentor is thinking..."):
            try:
                # System prompt for trading mentor personality
                system_prompt = """You are a professional trading mentor at Hantec Markets. Your role is to educate traders with clear, concise guidance.

**Your Communication Style:**
- Keep answers SHORT: 3-5 sentences maximum (50-80 words)
- Use simple language, avoid jargon unless explaining it
- Break complex topics into digestible steps
- Be encouraging and supportive
- Focus on practical, actionable advice
- Include specific examples when helpful

**Your Expertise:**
- Forex trading, CFDs, commodities
- Technical analysis & chart reading
- Risk management & psychology
- Trading strategies for beginners to intermediate

**Important Rules:**
1. NEVER give specific trade recommendations (buy/sell signals)
2. Always emphasize risk management
3. Remind users trading involves risk
4. Be educational, not advisory
5. If asked about specific instruments, give general market education instead

**Format:**
- Start with a direct answer
- Add 1-2 supporting points
- End with a practical tip or next step

Remember: You're a mentor teaching concepts, not a financial advisor giving recommendations."""

                # Call OpenAI API
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *[{"role": m["role"], "content": m["content"]} 
                          for m in st.session_state.messages[-5:]],  # Last 5 messages for context
                    ],
                    temperature=0.7,
                    max_tokens=150  # Keep responses concise
                )
                
                # Extract response
                assistant_message = response.choices[0].message.content
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                # Display assistant message
                st.markdown(f"""
                    <div class="chat-message assistant-message">
                        <strong>🤖 Trading Mentor:</strong><br>{assistant_message}
                    </div>
                """, unsafe_allow_html=True)
                
                # Show usage stats in expander
                with st.expander("📊 Response Stats"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Tokens", response.usage.total_tokens)
                    with col2:
                        cost = response.usage.total_tokens * 0.0000015
                        st.metric("Cost", f"${cost:.6f}")
                    with col3:
                        words = len(assistant_message.split())
                        st.metric("Words", words)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Make sure your API key is valid and you have credits available.")
    
    # Force refresh to show new messages
    st.rerun()

# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p>⚠️ <strong>Disclaimer:</strong> This AI mentor provides educational content only. 
        Trading involves substantial risk. Always do your own research and consult licensed financial advisors.</p>
        <p style='margin-top: 10px;'>
            <strong>Hantec Markets</strong> | Powered by OpenAI GPT-4o-mini | 
            <a href='https://www.hantecmarkets.com' target='_blank' style='color: #1e3c72;'>Visit Our Website</a>
        </p>
    </div>
""", unsafe_allow_html=True)

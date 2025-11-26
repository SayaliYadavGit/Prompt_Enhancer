from openai import OpenAI
import streamlit as st
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Hantec AI Mentor",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS matching both UIs
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #fafafa;
        padding: 0;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Thread header */
    .thread-header {
        background: white;
        padding: 16px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    .thread-title {
        font-size: 18px;
        font-weight: 600;
        color: #1a202c;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .thread-badge {
        background: #fee;
        color: #c53030;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 500;
    }
    
    .thread-close {
        color: #718096;
        cursor: pointer;
        font-size: 20px;
    }
    
    /* Chat message bubbles */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px 0;
    }
    
    .message-row {
        display: flex;
        gap: 16px;
        margin-bottom: 24px;
        align-items: flex-start;
    }
    
    .message-row.user {
        flex-direction: row-reverse;
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #2d3748;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 16px;
        flex-shrink: 0;
    }
    
    .message-avatar.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .message-content {
        flex: 1;
        max-width: 70%;
    }
    
    .message-bubble {
        background: white;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        line-height: 1.6;
        color: #2d3748;
    }
    
    .message-row.user .message-bubble {
        background: #f7fafc;
        text-align: right;
    }
    
    .message-status {
        margin-top: 8px;
        font-size: 13px;
        color: #059669;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Quick action buttons */
    .quick-actions {
        display: flex;
        gap: 12px;
        margin: 24px 0;
        flex-wrap: wrap;
    }
    
    .quick-action-btn {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 12px 20px;
        border-radius: 24px;
        font-size: 14px;
        color: #2d3748;
        cursor: pointer;
        transition: all 0.2s;
        white-space: nowrap;
    }
    
    .quick-action-btn:hover {
        background: #f7fafc;
        border-color: #cbd5e0;
        transform: translateY(-1px);
    }
    
    /* Chat input */
    .stTextInput > div > div > input {
        border-radius: 16px;
        padding: 18px 24px;
        border: 1px solid #e2e8f0;
        font-size: 15px;
        transition: all 0.3s ease;
        background-color: white;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8B0000;
        box-shadow: 0 0 0 3px rgba(139, 0, 0, 0.1);
    }
    
    /* Welcome screen styles */
    .welcome-section {
        text-align: center;
        padding: 60px 20px 50px 20px;
    }
    
    .logo-circle {
        width: 90px;
        height: 90px;
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        border-radius: 50%;
        margin: 0 auto 25px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 36px;
        color: white;
        font-weight: 700;
        font-style: italic;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }
    
    .welcome-title {
        font-size: 36px;
        font-weight: 600;
        color: #1a202c;
        margin-bottom: 16px;
        line-height: 1.2;
    }
    
    .name-highlight {
        color: #8B0000;
    }
    
    .welcome-subtitle {
        font-size: 17px;
        color: #64748b;
        margin-bottom: 50px;
        font-weight: 400;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    /* Disclaimer */
    .chat-disclaimer {
        text-align: center;
        font-size: 13px;
        color: #94a3b8;
        margin-top: 16px;
    }
    
    .chat-disclaimer a {
        color: #3b82f6;
        text-decoration: none;
    }
    
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🔑 API Configuration")
    api_key = st.text_input(
        "Enter your OpenAI API Key",
        type="password",
        help="Get your API key from https://platform.openai.com/api-keys",
        key="api_key_input"
    )
    
    if api_key:
        st.success("✓ API key connected", icon="✅")
    else:
        st.warning("⚠ Please enter your API key", icon="⚠️")
    
    st.markdown("---")
    
    st.markdown("### 👤 User Settings")
    user_name = st.text_input("Your Name", value="James", key="user_name")
    user_language = st.selectbox(
        "Preferred Language",
        ["English", "Spanish", "Portuguese", "Chinese", "Japanese", "Korean", "Thai"],
        key="language"
    )
    
    st.markdown("---")
    
    st.markdown("### 🎯 Current Session")
    if 'conversation_started' in st.session_state and st.session_state.conversation_started:
        st.info("Chat in progress")
        if st.button("← Back to Welcome"):
            st.session_state.conversation_started = False
            st.session_state.selected_option = None
            st.session_state.last_processed_message = ""
            st.rerun()
    else:
        st.caption("No active conversation")
    
    st.markdown("---")
    
    st.markdown("### 📚 Quick Links")
    st.markdown("- [Trading Guide](https://hantec.com/guide)")
    st.markdown("- [Risk Disclosure](https://hantec.com/risk)")
    st.markdown("- [Support Center](https://hantec.com/support)")
    st.markdown("- [Terms & Conditions](https://hantec.com/terms)")

# Initialize session state
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_state' not in st.session_state:
    st.session_state.user_state = "onboarding"
if 'onboarding_step' not in st.session_state:
    st.session_state.onboarding_step = 2
if 'last_processed_message' not in st.session_state:
    st.session_state.last_processed_message = ""
if 'processing' not in st.session_state:
    st.session_state.processing = False

import re

# Function to clean HTML tags from text
def clean_html_tags(text):
    """Remove any HTML tags from text"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

# Function to get system prompt with CC-SC-R framework
def get_system_prompt(user_context):
    return f"""You are the Hantec Markets AI Mentor, a conversational assistant guiding users through CFD trading.

USER CONTEXT:
- User State: {user_context['state']}
- Onboarding Step: {user_context['step']}/9
- Language: {user_context['language']}
- Name: {user_context['name']}
- Selected Path: {user_context.get('path', 'General')}

CRITICAL CONSTRAINTS:
- NEVER mention guaranteed returns
- NO financial advice (education only)
- ALWAYS include risk disclaimers for trading queries
- NO PII storage or repetition
- FSC (Mauritius) compliant responses only

RESPONSE STRUCTURE:
- Keep answers SHORT (2-4 sentences max)
- Use bullet points when listing items
- Use **bold** for emphasis
- Include ⚠️ for warnings
- Add links with [Link text →]
- NEVER use HTML tags like <div>, <span>, etc. - use only plain text and markdown

PERSONALITY:
- Knowledgeable but humble
- Empowering and motivational
- Transparent about limitations
- Patient, never condescending
- Conversational and friendly

MANDATORY DISCLAIMERS:
For trading queries: "⚠️ Trading involves risk. This is for educational purposes only."

BEHAVIOR:
- If unclear query: "I didn't understand. Can we try this again?"
- For onboarding users: Guide through incomplete steps
- For active traders: Provide market insights and platform help
- Celebrate milestones: "Great job completing KYC! 🎉"

Remember: You're a mentor, not a financial advisor. Keep it conversational, helpful, and compliant."""

# MAIN CONTENT LOGIC
# Show welcome screen OR conversation interface
if not st.session_state.conversation_started:
    # ==================== WELCOME SCREEN ====================
    
    st.markdown(f"""
        <div class="welcome-section">
            <div class="logo-circle">H</div>
            <div class="welcome-title">Welcome to Hantec one, <span class="name-highlight">{user_name}</span> 👋</div>
            <div class="welcome-subtitle">Pick an option below to continue — or ask me anything to get started</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Three option cards
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #8B0000 0%, #B22222 100%); 
                        color: white; 
                        padding: 32px; 
                        border-radius: 16px; 
                        min-height: 220px;
                        box-shadow: 0 4px 12px rgba(139, 0, 0, 0.2);
                        position: relative;">
                <div style="font-size: 28px; margin-bottom: 16px;">🚀</div>
                <div style="font-size: 22px; font-weight: 600; margin-bottom: 14px; line-height: 1.3;">
                    Start Live Trading
                </div>
                <div style="font-size: 15px; line-height: 1.6; opacity: 0.95; margin-bottom: 20px;">
                    Tell me your goal and account preferences — I'll set up your account to start trading
                </div>
                <div style="text-align: right; font-size: 28px; opacity: 0.7;">→</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Select", key="btn_start_trading", use_container_width=True):
            st.session_state.selected_option = "start_trading"
            st.session_state.conversation_started = True
            # Add initial AI message
            st.session_state.chat_history = [
                {
                    "role": "assistant", 
                    "content": f"Awesome, {user_name}! Let's get you started 💝\n\nBefore we begin — can you tell me how familiar you are with trading? Pick one below"
                }
            ]
            st.rerun()
    
    with col2:
        st.markdown("""
            <div style="background: white; 
                        padding: 32px; 
                        border-radius: 16px; 
                        min-height: 220px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                        border: 1px solid #e2e8f0;">
                <div style="font-size: 28px; margin-bottom: 16px;">📚</div>
                <div style="font-size: 22px; font-weight: 600; margin-bottom: 18px; color: #1a202c; line-height: 1.3;">
                    Learn CFDs
                </div>
                <div style="font-size: 15px; color: #64748b; line-height: 2;">
                    📊 Master the fundamentals<br>
                    📈 Try simple examples<br>
                    📉 Level up your skills
                </div>
                <div style="text-align: right; margin-top: 16px; font-size: 28px; color: #cbd5e0;">→</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Select", key="btn_learn_cfds", use_container_width=True):
            st.session_state.selected_option = "learn_cfds"
            st.session_state.conversation_started = True
            st.session_state.chat_history = [
                {
                    "role": "assistant",
                    "content": f"Great choice, {user_name}! Let's build your trading knowledge 📚\n\nWhat's your current experience level with CFD trading?"
                }
            ]
            st.rerun()
    
    with col3:
        st.markdown("""
            <div style="background: white; 
                        padding: 32px; 
                        border-radius: 16px; 
                        min-height: 220px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                        border: 1px solid #e2e8f0;">
                <div style="font-size: 28px; margin-bottom: 16px;">💬</div>
                <div style="font-size: 22px; font-weight: 600; margin-bottom: 14px; color: #1a202c; line-height: 1.3;">
                    Take a Quick Tour
                </div>
                <div style="font-size: 15px; color: #64748b; line-height: 1.6; margin-bottom: 20px;">
                    A quick walkthrough of your dashboard, features and charts
                </div>
                <div style="text-align: right; font-size: 28px; color: #cbd5e0;">→</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Select", key="btn_take_tour", use_container_width=True):
            st.session_state.selected_option = "take_tour"
            st.session_state.conversation_started = True
            st.session_state.chat_history = [
                {
                    "role": "assistant",
                    "content": f"Perfect, {user_name}! I'll show you around 🗺️\n\nLet me give you a tour of your Hantec dashboard. Where would you like to start?"
                }
            ]
            st.rerun()
    
    # Chat input on welcome screen
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col_input, col_mic = st.columns([20, 1])
    with col_input:
        welcome_input = st.text_input(
            "Chat",
            placeholder="Ask me anything...",
            key="welcome_chat_input",
            label_visibility="collapsed"
        )
    with col_mic:
        st.markdown("<div style='padding-top: 8px; font-size: 20px; color: #94a3b8;'>🎤</div>", unsafe_allow_html=True)
    
    if welcome_input and welcome_input != st.session_state.last_processed_message:
        if not api_key:
            st.error("❌ Please enter your OpenAI API key in the sidebar to chat", icon="🔒")
        else:
            # Mark as processing
            st.session_state.last_processed_message = welcome_input
            st.session_state.conversation_started = True
            st.session_state.selected_option = "general"
            
            # Add user message
            st.session_state.chat_history = [
                {"role": "user", "content": welcome_input}
            ]
            
            # Generate AI response
            try:
                client = OpenAI(api_key=api_key)
                
                user_context = {
                    'state': st.session_state.user_state,
                    'step': st.session_state.onboarding_step,
                    'language': user_language,
                    'name': user_name,
                    'path': 'general'
                }
                
                system_prompt = get_system_prompt(user_context)
                
                with st.spinner("🤖 AI Mentor is thinking..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": welcome_input}
                        ],
                        temperature=0.7,
                        max_tokens=400
                    )
                    
                    assistant_response = response.choices[0].message.content
                    # Clean any HTML tags from the response
                    assistant_response = clean_html_tags(assistant_response)
                    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                
                st.rerun()
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}", icon="⚠️")
                st.session_state.conversation_started = False
    
    st.markdown("""
        <div class="chat-disclaimer">
            All chats are private & encrypted. Hpulse may make mistakes — verify 
            <a href="#" target="_blank">Key Info ↗</a>
        </div>
    """, unsafe_allow_html=True)

else:
    # ==================== CONVERSATION INTERFACE ====================
    
    # Thread header
    thread_titles = {
        "start_trading": "Start Live Trading",
        "learn_cfds": "Learn CFDs",
        "take_tour": "Take a Quick Tour",
        "general": "Getting started!"
    }
    
    thread_title = thread_titles.get(st.session_state.selected_option, "Chat")
    
    col_header, col_close = st.columns([10, 1])
    with col_header:
        st.markdown(f"""
            <div class="thread-header">
                <div class="thread-title">
                    <span>▼</span>
                    <span>{thread_title}</span>
                    <span class="thread-badge">Current</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_close:
        if st.button("✕", key="close_thread"):
            st.session_state.conversation_started = False
            st.session_state.chat_history = []
            st.session_state.last_processed_message = ""
            st.rerun()
    
    # Chat messages display
    
    # Display chat history
    for i, msg in enumerate(st.session_state.chat_history):
        if msg["role"] == "assistant":
            # Show "Done✅" only if this is not the last message  
            status_html = '<div class="message-status">Done✅</div>' if i < len(st.session_state.chat_history) - 1 else ''
            
            st.markdown(f"""
                <div class="message-row">
                    <div class="message-avatar">H</div>
                    <div class="message-content">
                        <div class="message-bubble">{msg['content']}</div>
                        {status_html}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="message-row user">
                    <div class="message-avatar user">{user_name[0]}</div>
                    <div class="message-content">
                        <div class="message-bubble">{msg['content']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Quick action buttons (show after first AI message)
    if len(st.session_state.chat_history) == 1 and st.session_state.selected_option == "start_trading":
        
        col_q1, col_q2, col_q3, col_q4 = st.columns([1.5, 2, 1.8, 0.3])
        
        with col_q1:
            if st.button("I'm completely new", key="qa_new"):
                st.session_state.chat_history.append({"role": "user", "content": "I'm completely new"})
                st.rerun()
        
        with col_q2:
            if st.button("Open a demo account and practice", key="qa_demo"):
                st.session_state.chat_history.append({"role": "user", "content": "Open a demo account and practice"})
                st.rerun()
        
        with col_q3:
            if st.button("Try a quick product demo", key="qa_product"):
                st.session_state.chat_history.append({"role": "user", "content": "Try a quick product demo"})
                st.rerun()
        
        with col_q4:
            st.markdown("<div style='padding-top: 8px; font-size: 20px; color: #cbd5e0;'>→</div>", unsafe_allow_html=True)
    
    # Chat input
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_input, col_mic = st.columns([20, 1])
    
    with col_input:
        user_input = st.text_input(
            "Message",
            placeholder="Ask me anything...",
            key="chat_input_field",
            label_visibility="collapsed"
        )
    
    with col_mic:
        st.markdown("<div style='padding-top: 8px; font-size: 20px; color: #94a3b8;'>🎤</div>", unsafe_allow_html=True)
    
    # Process chat input
    if user_input and user_input != st.session_state.last_processed_message:
        if not api_key:
            st.error("❌ Please enter your OpenAI API key in the sidebar", icon="🔒")
        else:
            try:
                # Prevent duplicate processing
                st.session_state.last_processed_message = user_input
                
                client = OpenAI(api_key=api_key)
                
                # Build user context
                user_context = {
                    'state': st.session_state.user_state,
                    'step': st.session_state.onboarding_step,
                    'language': user_language,
                    'name': user_name,
                    'path': st.session_state.selected_option
                }
                
                # Get system prompt
                system_prompt = get_system_prompt(user_context)
                
                # Add user message
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                with st.spinner("🤖 AI Mentor is thinking..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            *st.session_state.chat_history[-10:]
                        ],
                        temperature=0.7,
                        max_tokens=400
                    )
                    
                    assistant_response = response.choices[0].message.content
                    # Clean any HTML tags from the response
                    assistant_response = clean_html_tags(assistant_response)
                    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                
                st.rerun()
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}", icon="⚠️")
                st.session_state.last_processed_message = ""  # Reset on error
    
    # Disclaimer
    st.markdown("""
        <div class="chat-disclaimer">
            All chats are private & encrypted. Hpulse may make mistakes — verify 
            <a href="#" target="_blank">Key Info ↗</a>
        </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_clear, col_export, col_support = st.columns(3)
    
    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.conversation_started = False
            st.session_state.last_processed_message = ""
            st.rerun()
    
    with col_export:
        if st.session_state.chat_history:
            chat_export = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button(
                label="📥 Export",
                data=chat_export,
                file_name=f"hantec_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    with col_support:
        if st.button("👤 Contact Support", use_container_width=True):
            st.info("Connecting to support...", icon="📞")

# Footer
st.markdown("---")
st.caption("""
**Risk Warning:** CFDs are complex instruments and come with a high risk of losing money rapidly due to leverage. 
Hantec Markets is licensed by FSC (Mauritius). This AI provides educational information only, not financial advice.
""")

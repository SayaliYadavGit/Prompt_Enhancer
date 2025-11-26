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

# Custom CSS to match the UI design exactly
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
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Welcome section */
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
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Button styling */
    .stButton > button {
        padding: 0;
        border: none;
        background: none;
        width: 100%;
        height: 100%;
    }
    
    /* Card container for grid */
    div[data-testid="column"] {
        padding: 0 10px;
    }
    
    /* Input styling */
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
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    /* Success/Info/Warning boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        padding: 20px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8fafc;
        border-radius: 8px;
        font-weight: 500;
    }
    
    </style>
""", unsafe_allow_html=True)

# Sidebar for API Key and Settings
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
    
    st.markdown("### 📚 Quick Links")
    st.markdown("- [Trading Guide](https://hantec.com/guide)")
    st.markdown("- [Risk Disclosure](https://hantec.com/risk)")
    st.markdown("- [Support Center](https://hantec.com/support)")
    st.markdown("- [Terms & Conditions](https://hantec.com/terms)")
    
    st.markdown("---")
    
    st.markdown("### ℹ️ About")
    st.caption("Hantec AI Mentor v1.0")
    st.caption("Powered by Claude API")
    st.caption("FSC (Mauritius) Licensed")

# Initialize session state
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_state' not in st.session_state:
    st.session_state.user_state = "onboarding"  # or "active_trader"
if 'onboarding_step' not in st.session_state:
    st.session_state.onboarding_step = 2  # Simulating step 2 of 9

# Function to detect user intent and provide appropriate response
def get_mentor_response(user_query, conversation_history, user_context):
    """Generate AI mentor response with CC-SC-R framework"""
    
    # Context: User state, onboarding progress, language
    context = f"""
    User State: {user_context['state']}
    Onboarding Step: {user_context['step']}/9
    Language: {user_context['language']}
    Name: {user_context['name']}
    """
    
    # Constraints: Regulatory, compliance, risk disclaimers
    constraints = """
    CRITICAL CONSTRAINTS:
    - NEVER mention guaranteed returns
    - NO financial advice (education only)
    - ALWAYS include risk disclaimers for trading queries
    - NO PII storage or repetition
    - Responses must be compliant with FSC (Mauritius) regulations
    - Block any harmful or non-compliant requests
    """
    
    # Structure: Response format requirements
    structure = """
    RESPONSE STRUCTURE:
    - Keep answers SHORT and PRECISE (3-5 sentences max)
    - Use bullet points, NOT paragraphs
    - Use **bold** for emphasis
    - Include relevant links with [Link text →]
    - Add ⚠️ for warnings
    - Format with ## for titles, ### for subtitles
    """
    
    # Checkpoints: Confidence and risk assessment
    checkpoint = """
    BEFORE RESPONDING:
    1. Identify confidence level (High/Medium/Low)
    2. Check for regulatory risk
    3. Check for financial risk
    4. Check for reputational risk
    5. If confidence < 80%, redirect to support
    """
    
    # Review: Mandatory disclaimers
    review = """
    MANDATORY DISCLAIMERS:
    - Trading-related: "⚠️ Trading involves risk. This is for educational purposes only."
    - Not advice: "This is not financial advice."
    - External data: "Data source: [Provider Name]"
    """
    
    system_prompt = f"""You are the Hantec Markets AI Mentor, a conversational assistant guiding users through CFD trading.

{context}

{constraints}

{structure}

{checkpoint}

{review}

PERSONALITY:
- Knowledgeable but humble
- Empowering and motivational
- Transparent about limitations
- Patient and never condescending
- Celebrate user milestones

KNOWLEDGE PRIORITY (NEVER OVERRIDE):
1. Official product guides & regulatory T&Cs
2. KYC/AML procedures
3. Hantec-verified documentation
4. External sources (clearly attributed)
5. Redirect complex queries to support

If user query is unclear, respond: "I didn't understand. Can we try this again?"

For onboarding users, guide them step-by-step through incomplete stages.
For active traders, provide trade ideas, platform help, and market insights.
"""
    
    return system_prompt

# Main content starts here

# Welcome Section with logo and greeting
st.markdown(f"""
    <div class="welcome-section">
        <div class="logo-circle">H</div>
        <div class="welcome-title">Welcome to Hantec one, <span class="name-highlight">{user_name}</span> 👋</div>
        <div class="welcome-subtitle">Pick an option below to continue — or ask me anything to get started</div>
    </div>
""", unsafe_allow_html=True)

# Three option cards in columns
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    # Primary card - Start Live Trading
    st.markdown("""
        <div style="background: linear-gradient(135deg, #8B0000 0%, #B22222 100%); 
                    color: white; 
                    padding: 32px; 
                    border-radius: 16px; 
                    min-height: 220px;
                    box-shadow: 0 4px 12px rgba(139, 0, 0, 0.2);
                    cursor: pointer;
                    transition: all 0.3s ease;
                    position: relative;
                    overflow: hidden;">
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
    
    if st.button("Select Start Live Trading", key="btn_start_trading", use_container_width=True):
        st.session_state.selected_option = "start_trading"
        st.rerun()

with col2:
    # Secondary card - Learn CFDs
    st.markdown("""
        <div style="background: white; 
                    padding: 32px; 
                    border-radius: 16px; 
                    min-height: 220px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                    border: 1px solid #e2e8f0;
                    cursor: pointer;
                    transition: all 0.3s ease;">
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
    
    if st.button("Select Learn CFDs", key="btn_learn_cfds", use_container_width=True):
        st.session_state.selected_option = "learn_cfds"
        st.rerun()

with col3:
    # Tertiary card - Take a Tour
    st.markdown("""
        <div style="background: white; 
                    padding: 32px; 
                    border-radius: 16px; 
                    min-height: 220px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                    border: 1px solid #e2e8f0;
                    cursor: pointer;
                    transition: all 0.3s ease;">
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
    
    if st.button("Select Take a Tour", key="btn_take_tour", use_container_width=True):
        st.session_state.selected_option = "take_tour"
        st.rerun()

# Display selected option content
if st.session_state.selected_option:
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.selected_option == "start_trading":
        st.markdown("### 🚀 Let's Get You Started with Live Trading")
        
        # Onboarding progress
        progress = st.session_state.onboarding_step / 9
        st.progress(progress)
        st.caption(f"Step {st.session_state.onboarding_step} of 9 completed")
        
        st.info(f"""
        **Hi {user_name}!** I can see you haven't completed onboarding yet. Let's get you set up to trade.
        
        **Your Progress:**
        1. ✅ Account created
        2. ⏳ **Upload ID verification** ← You are here
        3. ⏳ Address verification
        4. ⏳ Employment details
        5. ⏳ Create MT4/MT5 account
        6. ⏳ Email verification
        7. ⏳ KYC approval
        8. ⏳ First deposit
        9. ⏳ Start trading
        
        **What you need now:**
        - Valid government ID (passport/driver's license)
        - Clear photo or scan
        
        [Upload ID now →](#)
        
        Need help with what documents are accepted? Just ask!
        """, icon="ℹ️")
    
    elif st.session_state.selected_option == "learn_cfds":
        st.markdown("### 📚 Learn CFD Trading")
        
        st.success(f"""
        **Welcome to CFD Trading Education, {user_name}!**
        
        Let's create your personalized learning plan. First, tell me about yourself:
        
        **Quick Questions:**
        - How many years of trading experience do you have?
        - What is your age?
        - How much risk can you take?
        
        Based on your answers, I'll create a curated tutorial for you.
        """, icon="📚")
        
        # Learning path options
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("**🌱 Beginner**")
            st.caption("Start with fundamentals")
        with col_b:
            st.markdown("**📊 Intermediate**")
            st.caption("Trading strategies")
        with col_c:
            st.markdown("**🎯 Advanced**")
            st.caption("Technical analysis")
    
    elif st.session_state.selected_option == "take_tour":
        st.markdown("### 🗺️ Dashboard Tour")
        
        st.info(f"""
        **Hi {user_name}, I'm your tour assistant!**
        
        Let's walk you through Hantec's dashboard. Here's what you'll find:
        
        **Key Features:**
        - 📊 **Live Charts** - Real-time market data and pricing
        - 💼 **Portfolio** - Your positions and performance
        - 📈 **Trade Ideas** - Expert analysis and signals
        - ⚙️ **Settings** - Customize your experience
        - 📱 **Mobile App** - Trade on the go
        
        Ready to explore? Which area would you like to see first?
        """, icon="🗺️")

# Spacer
st.markdown("<br>", unsafe_allow_html=True)

# Chat Interface Section
st.markdown("### 💬 Ask Me Anything")

# Chat input with microphone icon
col_input, col_mic = st.columns([20, 1])

with col_input:
    user_input = st.text_input(
        "Chat input",
        placeholder="Ask me anything...",
        key="chat_input_field",
        label_visibility="collapsed"
    )

with col_mic:
    st.markdown("<div style='padding-top: 8px; font-size: 20px; color: #94a3b8;'>🎤</div>", unsafe_allow_html=True)

# Process chat input
if user_input:
    if not api_key:
        st.error("❌ Please enter your OpenAI API key in the sidebar to use the AI Mentor.", icon="🔒")
    else:
        try:
            client = OpenAI(api_key=api_key)
            
            # Build user context
            user_context = {
                'state': st.session_state.user_state,
                'step': st.session_state.onboarding_step,
                'language': user_language,
                'name': user_name
            }
            
            # Get system prompt with CC-SC-R framework
            system_prompt = get_mentor_response(user_input, st.session_state.chat_history, user_context)
            
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            with st.spinner("🤖 AI Mentor is thinking..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *st.session_state.chat_history[-10:]  # Last 5 exchanges
                    ],
                    temperature=0.7,
                    max_tokens=600
                )
                
                assistant_response = response.choices[0].message.content
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
            
            # Display conversation
            st.markdown("---")
            
            # Show last 6 messages (3 exchanges)
            for i, msg in enumerate(st.session_state.chat_history[-6:]):
                if msg["role"] == "user":
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(msg['content'])
                    
                if i < len(st.session_state.chat_history[-6:]) - 1:
                    st.markdown("<br>", unsafe_allow_html=True)
            
            # API usage details
            with st.expander("📊 API Usage Details"):
                st.write(f"**Model:** {response.model}")
                st.write(f"**Tokens Used:** {response.usage.total_tokens}")
                st.write(f"**Prompt Tokens:** {response.usage.prompt_tokens}")
                st.write(f"**Completion Tokens:** {response.usage.completion_tokens}")
                st.write(f"**Estimated Cost:** ${response.usage.total_tokens * 0.0000015:.6f}")
                st.caption("GPT-4o-mini: $0.150 per 1M input tokens, $0.600 per 1M output tokens")
        
        except Exception as e:
            st.error(f"❌ Error calling OpenAI API: {str(e)}", icon="⚠️")
            st.info("💡 Please verify your API key is valid and has available credits.")

# Chat disclaimer
st.markdown("""
    <div style="text-align: center; margin-top: 16px; font-size: 13px; color: #94a3b8;">
        All chats are private & encrypted. Hpulse may make mistakes — verify 
        <a href="#" style="color: #3b82f6; text-decoration: none;">Key Info ↗</a>
    </div>
""", unsafe_allow_html=True)

# Action buttons
st.markdown("<br>", unsafe_allow_html=True)

col_clear, col_export, col_escalate = st.columns([1, 1, 1])

with col_clear:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.selected_option = None
        st.rerun()

with col_export:
    if st.session_state.chat_history:
        chat_export = json.dumps(st.session_state.chat_history, indent=2)
        st.download_button(
            label="📥 Export Chat",
            data=chat_export,
            file_name=f"hantec_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

with col_escalate:
    if st.button("👤 Contact Support", use_container_width=True):
        st.info("Connecting you to a human support agent... [Support Portal →](#)", icon="📞")

# Footer with compliance info
st.markdown("---")
st.caption("""
**Risk Warning:** CFDs are complex instruments and come with a high risk of losing money rapidly due to leverage. 
You should consider whether you understand how CFDs work and whether you can afford to take the high risk of losing your money.

**Regulatory Information:** Hantec Markets is licensed and regulated by the Financial Services Commission (FSC) of Mauritius.

This AI assistant provides educational information only and does not constitute financial advice.
""")

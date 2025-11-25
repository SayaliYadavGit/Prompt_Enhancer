import streamlit as st
from openai import OpenAI

# ========================================
# PAGE CONFIGURATION
# ========================================
st.set_page_config(page_title="Prompt Enhancer", page_icon="📝")
st.title("📝 Prompt Engineer — General Prompt Enhancer")

# ========================================
# API KEY INPUT (Manual Entry)
# ========================================
st.sidebar.header("🔑 API Configuration")
api_key = st.sidebar.text_input(
    "Enter your OpenAI API Key:",
    type="password",
    help="Your API key starts with 'sk-proj-...' Get it from https://platform.openai.com/api-keys"
)

# Show status indicator
if api_key:
    if api_key.startswith('sk-'):
        st.sidebar.success("✅ API Key entered")
        # Create OpenAI client with the entered key
        try:
            client = OpenAI(api_key=api_key)
            api_key_valid = True
        except Exception as e:
            st.sidebar.error("❌ Invalid API key format")
            api_key_valid = False
    else:
        st.sidebar.warning("⚠️ API key should start with 'sk-'")
        api_key_valid = False
else:
    st.sidebar.info("ℹ️ Enter API key to use Live Mode")
    api_key_valid = False

# ========================================
# MODE SELECTION
# ========================================
if api_key_valid:
    mode = st.radio(
        "Select Mode:", 
        ["Demo Mode (Free)", "Live Mode (Uses API)"], 
        horizontal=True
    )
else:
    mode = "Demo Mode (Free)"
    st.info("💡 Enter your API key in the sidebar to enable Live Mode")

if mode == "Demo Mode (Free)":
    st.caption("Demo Mode - Learn how to structure better prompts!")
else:
    st.caption("🟢 Live Mode - Using real OpenAI API")

# ========================================
# CC-SC-R FRAMEWORK INPUTS
# ========================================
st.subheader("Enter CC-SC-R Framework")

col1, col2 = st.columns(2)

with col1:
    Context = st.text_area(
        "Context requirements", 
        value="Domain audience goal...",
        height=80,
        help="Who is this for? What's the domain? What's the goal?"
    )
    
    Constraints = st.text_area(
        "Constraints specifications", 
        value="Policies, Compliance and regulatory limits...",
        height=80,
        help="What limitations exist? Policies, regulations, budget?"
    )
    
    Structure = st.text_area(
        "Structure Mandates", 
        value="Required sections fields and formatting...",
        height=80,
        help="Required format, sections, or structure?"
    )

with col2:
    Checkpoint = st.text_area(
        "Checkpoint Integration", 
        value="Assumptions, Risks, Confidence levels...",
        height=80,
        help="What assumptions to validate? What risks to flag?"
    )
    
    Review = st.text_area(
        "Review Protocols", 
        value="Approval points and escalation triggers...",
        height=80,
        help="Who reviews? When to escalate?"
    )

# ========================================
# DRAFT PROMPT INPUT
# ========================================
st.subheader("Paste your rough prompt")
draft = st.text_area(
    "Your draft prompt:", 
    height=140,
    placeholder="Example: Write a blog post about AI...",
    help="Enter your initial prompt that needs enhancement"
)

# ========================================
# ENHANCE BUTTON & LOGIC
# ========================================
if st.button("🚀 Enhance Prompt", type="primary", use_container_width=True):
    if not draft.strip():
        st.warning("⚠️ Please enter a draft prompt.")
    
    else:
        # ==================================================
        # DEMO MODE - Shows structure without API call
        # ==================================================
        if mode == "Demo Mode (Free)":
            instruction = (
                "Generate an enhanced, structured prompt using CC-SC-R.\n"
                "1) Improve clarity and completeness\n"
                "2) Ask ONE clarifying question\n"
                "3) Specify output format (3 bullets, ≤12 words each)\n"
            )
            demo_output = (
                f"**Context:** {Context}\n\n"
                f"**Constraints:** {Constraints}\n\n"
                f"**Structure:** {Structure}\n\n"
                f"**Checkpoints:** {Checkpoint}\n\n"
                f"**Review:** {Review}\n\n"
                f"**USER DRAFT:**\n{draft}\n\n"
                "**OUTPUT FORMAT:**\n- 3 concise bullets\n- 1 clarifying question"
            )
            
            st.success("✅ Enhanced Prompt Structure (Demo Mode)")
            st.markdown("---")
            st.markdown("### Framework Applied:")
            st.code(instruction, language="markdown")
            st.markdown("### Your Structured Prompt:")
            st.markdown(demo_output)
            st.info("💡 This is demo mode showing the CC-SC-R structure. Switch to Live Mode to get AI-enhanced prompts!")
        
        # ==================================================
        # LIVE MODE - Real OpenAI API call
        # ==================================================
        else:
            if not api_key_valid:
                st.error("❌ Please enter a valid API key in the sidebar to use Live Mode")
            else:
                try:
                    with st.spinner("🤖 AI is enhancing your prompt..."):
                        # Construct the system prompt
                        system_prompt = """You are an expert prompt engineer specializing in the CC-SC-R framework 
                        (Context, Constraints, Structure, Checkpoints, Review).
                        
                        Your task:
                        1. Analyze the user's draft prompt and CC-SC-R inputs
                        2. Enhance the prompt for clarity, completeness, and effectiveness
                        3. Apply the CC-SC-R framework systematically
                        4. Ask ONE clarifying question to improve the prompt further
                        5. Format output clearly
                        
                        Be concise, professional, and actionable."""
                        
                        # Construct the user message
                        user_message = f"""Please enhance this prompt using the CC-SC-R framework:

**Context:** {Context}

**Constraints:** {Constraints}

**Structure:** {Structure}

**Checkpoints:** {Checkpoint}

**Review:** {Review}

**User's Draft Prompt:**
{draft}

**Instructions:**
1. Generate an enhanced, production-ready prompt incorporating all CC-SC-R elements
2. Make it clear, actionable, and comprehensive
3. Ask ONE specific clarifying question to further improve it
4. Format the enhanced prompt in a structured way

**Output Format:**
- Enhanced Prompt (full text with CC-SC-R integrated)
- Clarifying Question (1 specific question)
- Key Improvements (3 bullets, ≤12 words each)"""

                        # Call OpenAI API
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_message}
                            ],
                            temperature=0.7,
                            max_tokens=1000
                        )
                        
                        # Extract the AI's response
                        enhanced_prompt = response.choices[0].message.content
                        
                        # Display results
                        st.success("✅ Prompt Enhanced by AI!")
                        st.markdown("---")
                        st.markdown(enhanced_prompt)
                        
                        # Show API usage info
                        with st.expander("📊 API Usage Details"):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Model", response.model)
                            with col2:
                                st.metric("Tokens Used", response.usage.total_tokens)
                            with col3:
                                cost = response.usage.total_tokens * 0.0000015
                                st.metric("Cost", f"${cost:.6f}")
                            
                            st.caption("💰 GPT-4o-mini: $0.150 per 1M input tokens, $0.600 per 1M output tokens")
                        
                        # Download button for enhanced prompt
                        st.download_button(
                            label="📥 Download Enhanced Prompt",
                            data=enhanced_prompt,
                            file_name="enhanced_prompt.txt",
                            mime="text/plain"
                        )
                
                except Exception as e:
                    st.error(f"❌ Error calling OpenAI API: {str(e)}")
                    st.info("💡 Common issues:")
                    st.markdown("""
                    - Check your API key is correct
                    - Verify you have credits in your OpenAI account
                    - Ensure your API key has proper permissions
                    """)

# ========================================
# SIDEBAR - ADDITIONAL INFO
# ========================================
st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ About CC-SC-R")
st.sidebar.markdown("""
**Context:** Who, what, where, when, why?

**Constraints:** Limits, policies, regulations

**Structure:** Required format, sections

**Checkpoints:** Assumptions, risks to validate

**Review:** Approval process, escalation
""")

st.sidebar.markdown("---")
st.sidebar.subheader("💡 Tips")
st.sidebar.markdown("""
- Be specific in your draft prompt
- Fill in all CC-SC-R fields
- Use Live Mode for best results
- Download enhanced prompts for reuse
""")

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit + OpenAI API")

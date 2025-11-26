from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="Prompt Enhancer", page_icon="📝")

# Sidebar for API Key
with st.sidebar:
    st.header("🔑 API Configuration")
    api_key = st.text_input(
        "Enter your OpenAI API Key",
        type="password",
        help="Get your API key from https://platform.openai.com/api-keys"
    )
    
    if api_key:
        st.success("API key provided ✓")
    else:
        st.warning("Please enter your API key to use Live Mode")
    
    st.markdown("---")
    st.markdown("### How to get an API key:")
    st.markdown("1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)")
    st.markdown("2. Sign up or log in")
    st.markdown("3. Create a new API key")
    st.markdown("4. Copy and paste it above")

# Main app
st.title("📝 Prompt Engineer — General Prompt Enhancer")

# Add mode toggle at the top
mode = st.radio("Select Mode:", ["Demo Mode (Free)", "Live Mode (Uses API)"], horizontal=True)

if mode == "Demo Mode (Free)":
    st.caption("Demo Mode - Learn how to structure better prompts!")
else:
    st.caption("🟢 Live Mode - Using real OpenAI API")

st.subheader("Enter CC-SC-R Framework")
Context = st.text_input("Context requirements", value="Domain audience goal...")
Constraints = st.text_area("Constraints specifications", value="Policies, Compliance and regulatory limits...")
Structure = st.text_area("Structure Mandates", value="Required sections fields and formatting...")
Checkpoint = st.text_area("Checkpoint Integration", value="Assumptions, Risks, Confidence levels...")
Review = st.text_area("Review Protocols", value="Approval points and escalation triggers...")

st.subheader("Paste your rough prompt")
draft = st.text_area("Your draft prompt:", height=140)

if st.button("Enhance Prompt"):
    if not draft.strip():
        st.warning("Please enter a draft prompt.")
    else:
        # ==================================================
        # DEMO MODE - Shows structure without API call
        # ==================================================
        if mode == "Demo Mode (Free)":
            instruction = (
                "Generate an enhanced, structured prompt using CC-SCR-R.\n"
                "1) Improve clarity and completeness\n"
                "2) Ask ONE clarifying question\n"
                "3) Specify output format (3 bullets, ≤12 words each)\n"
            )
            demo_output = (
                f"Context: {Context}\n"
                f"Constraints: {Constraints}\n"
                f"Structure: {Structure}\n"
                f"Checkpoints: {Checkpoint}\n"
                f"Review: {Review}\n\n"
                f"USER DRAFT:\n{draft}\n\n"
                "OUTPUT FORMAT:\n- 3 concise bullets\n- 1 clarifying question"
            )
            
            st.success("Enhanced Prompt (Demo Mode)")
            st.code(instruction + "\n" + demo_output, language="markdown")
            st.info("💡 This is demo mode showing the CC-SC-R structure. Switch to Live Mode to get AI-enhanced prompts!")
        
        # ==================================================
        # LIVE MODE - Real OpenAI API call
        # ==================================================
        else:
            # Check if API key is provided
            if not api_key:
                st.error("❌ Please enter your OpenAI API key in the sidebar to use Live Mode.")
            else:
                try:
                    # Create OpenAI client with the provided API key
                    client = OpenAI(api_key=api_key)
                    
                    with st.spinner("🤖 AI is enhancing your prompt..."):
                        # Construct the system prompt (tells AI how to behave)
                        system_prompt = """You are an expert prompt engineer specializing in the CC-SC-R framework 
                        (Context, Constraints, Structure, Checkpoints, Review).
                        
                        Your task:
                        1. Analyze the user's draft prompt and CC-SC-R inputs
                        2. Enhance the prompt for clarity, completeness, and effectiveness
                        3. Apply the CC-SC-R framework systematically
                        4. Ask ONE clarifying question to improve the prompt further
                        5. Format output as requested
                        
                        Be concise, professional, and actionable."""
                        
                        # Construct the user message (the actual request)
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
- Enhanced Prompt (full text)
- Clarifying Question (1 specific question)
- Key Improvements (3 bullets, ≤12 words each)"""

                        # Call OpenAI API
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",  # Fast and cost-effective model
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_message}
                            ],
                            temperature=0.7,  # Balance between creativity and consistency
                            max_tokens=800    # Limit response length
                        )
                        
                        # Extract the AI's response
                        enhanced_prompt = response.choices[0].message.content
                        
                        # Display results
                        st.success("✅ Prompt Enhanced by AI!")
                        st.markdown("---")
                        st.markdown(enhanced_prompt)
                        
                        # Show API usage info
                        with st.expander("📊 API Usage Details"):
                            st.write(f"**Model:** {response.model}")
                            st.write(f"**Tokens Used:** {response.usage.total_tokens}")
                            st.write(f"**Approximate Cost:** ${response.usage.total_tokens * 0.0000015:.6f}")
                            st.caption("(GPT-4o-mini: $0.150 per 1M input tokens, $0.600 per 1M output tokens)")
                    
                except Exception as e:
                    st.error(f"❌ Error calling OpenAI API: {str(e)}")
                    st.info("💡 Make sure your API key is valid and you have credits in your OpenAI account.")

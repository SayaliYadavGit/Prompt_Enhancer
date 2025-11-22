import streamlit as st
st.set_page_config(page_title="Prompt Enhancer", page_icon="📝")
st.title("📝 Prompt Engineer — General Prompt Enhancer")

st.caption("Demo Mode - Learn how to structure better prompts!")

st.subheader("Enter CC-SC-R")
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
        # Demo output - shows structured approach
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
        
        st.info("💡 This is demo mode showing the CC-SC-R structure. In live mode, AI would generate the actual enhanced prompt!")




"""
Hantec AI Mentor - RAG Implementation with ChromaDB
Compatible with Streamlit Cloud
Add your own knowledge files to data/knowledge_base/
Supports: .txt, .md, .json
"""

from openai import OpenAI
import streamlit as st
import json
from datetime import datetime
import os
import glob

# Page configuration
st.set_page_config(
    page_title="Hantec AI Mentor",
    page_icon="🤖",
    layout="wide"
)

# ============================================================================
# RAG SYSTEM - CHROMADB with Streamlit Cloud Fix
# ============================================================================

class HantecRAG:
    def __init__(self, knowledge_base_path="data/knowledge_base"):
        """Initialize ChromaDB and load knowledge from your files"""
        self.knowledge_base_path = knowledge_base_path
        
        # Create directory if it doesn't exist
        os.makedirs(knowledge_base_path, exist_ok=True)
        
        # Initialize ChromaDB - Updated for newer versions
        try:
            import chromadb
            from chromadb.utils import embedding_functions
            
            # Use ephemeral client for Streamlit Cloud (no persistence issues)
            self.client = chromadb.EphemeralClient()
            
            # Use default embedding function
            default_ef = embedding_functions.DefaultEmbeddingFunction()
            
            # Get or create collection
            try:
                # Try to get existing collection
                self.collection = self.client.get_collection(
                    name="hantec_knowledge",
                    embedding_function=default_ef
                )
            except:
                # Collection doesn't exist, create it
                self.collection = self.client.create_collection(
                    name="hantec_knowledge",
                    embedding_function=default_ef,
                    metadata={"hnsw:space": "cosine"}
                )
            
        except ImportError as e:
            st.error(f"ChromaDB import error: {e}")
            st.info("Install: pip install chromadb==0.4.22")
            raise
        except Exception as e:
            st.error(f"ChromaDB initialization error: {e}")
            raise
        
        # Load all knowledge files
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load all files from knowledge_base folder"""
        
        # Get all supported files
        txt_files = glob.glob(f"{self.knowledge_base_path}/**/*.txt", recursive=True)
        md_files = glob.glob(f"{self.knowledge_base_path}/**/*.md", recursive=True)
        json_files = glob.glob(f"{self.knowledge_base_path}/**/*.json", recursive=True)
        
        all_files = txt_files + md_files + json_files
        
        if not all_files:
            st.sidebar.warning(f"⚠️ No knowledge files found in {self.knowledge_base_path}")
            st.sidebar.info("📝 Add .txt, .md, or .json files to start!")
            return
        
        documents = []
        metadatas = []
        ids = []
        
        for file_path in all_files:
            try:
                # Read file content
                content = self._read_file(file_path)
                
                if content and content.strip():
                    # Extract file info
                    filename = os.path.basename(file_path)
                    file_ext = os.path.splitext(filename)[1]
                    category = os.path.basename(os.path.dirname(file_path))
                    
                    # Add to lists
                    documents.append(content)
                    metadatas.append({
                        "filename": filename,
                        "category": category,
                        "type": file_ext[1:]
                    })
                    ids.append(f"doc_{len(documents)}_{filename}")
                    
            except Exception as e:
                st.sidebar.error(f"Error loading {file_path}: {str(e)}")
        
        # Add all documents to collection
        if documents:
            try:
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                st.sidebar.success(f"✅ Loaded {len(documents)} documents")
            except Exception as e:
                st.sidebar.error(f"Error adding to ChromaDB: {str(e)}")
        else:
            st.sidebar.warning("⚠️ No valid content found")
    
    def _read_file(self, file_path):
        """Read content from different file types"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext in ['.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif file_ext == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return json.dumps(data, indent=2)
        except Exception as e:
            st.sidebar.error(f"Error reading {file_path}: {e}")
            return ""
        
        return ""
    
    def retrieve(self, query, n_results=3):
        """Retrieve relevant documents from knowledge base"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            if results and results.get('documents') and results['documents'][0]:
                retrieved_text = "\n\n---\n\n".join(results['documents'][0])
                
                sources = []
                if results.get('metadatas') and results['metadatas'][0]:
                    for meta in results['metadatas'][0]:
                        sources.append(f"{meta.get('category', 'unknown')}/{meta.get('filename', 'unknown')}")
                
                return retrieved_text, sources
            
            return "", []
            
        except Exception as e:
            st.sidebar.error(f"Retrieval error: {str(e)}")
            return "", []

# Initialize RAG system
@st.cache_resource
def get_rag_system():
    return HantecRAG()

# ============================================================================
# CC-SC-R FRAMEWORK
# ============================================================================

def build_system_prompt(user_context, retrieved_knowledge, sources):
    """Build complete system prompt with CC-SC-R framework"""
    
    source_info = ""
    if sources:
        source_info = f"\n\nSOURCES: {', '.join(sources)}"
    
    return f"""You are the Hantec Markets AI Mentor, a conversational assistant guiding users through CFD trading.

USER CONTEXT:
- Name: {user_context.get('name', 'User')}
- State: {user_context.get('state', 'unknown')}
- Onboarding Step: {user_context.get('step', 0)}/9
- Language: {user_context.get('language', 'English')}

CRITICAL CONSTRAINTS:
- NEVER mention guaranteed returns or promise profits
- NO financial advice - education only
- ALWAYS include risk disclaimers for trading queries
- NO storage or repetition of PII
- All responses must be FSC (Mauritius) compliant

RESPONSE STRUCTURE:
- Keep answers SHORT and PRECISE (2-4 sentences maximum)
- Use bullet points for lists
- Use **bold** for emphasis
- Include ⚠️ emoji for warnings
- When providing links, ALWAYS use hmarkets.com domain
- Use friendly, conversational tone

HANTEC KNOWLEDGE BASE:
{retrieved_knowledge if retrieved_knowledge else "No specific knowledge found - provide general guidance and suggest contacting support for details."}
{source_info}

MANDATORY DISCLAIMERS:
- For trading queries: "⚠️ Trading involves risk. This is for educational purposes only."
- For leverage: "Leverage magnifies both gains and losses"
- If unsure: Redirect to support@hmarkets.com or live chat

PERSONALITY:
- Knowledgeable but humble
- Empowering and motivational
- Transparent about limitations
- Patient, never condescending

Company website: hmarkets.com
Support: support@hmarkets.com | Live chat 24/5

Remember: You're a mentor, not a financial advisor. Keep it conversational, helpful, and compliant.
"""

# ============================================================================
# STREAMLIT UI
# ============================================================================

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    .main { background-color: #fafafa; }
    #MainMenu, footer, header { visibility: hidden; }
    
    .stTextInput > div > div > input {
        border-radius: 16px;
        padding: 18px 24px;
        border: 1px solid #e2e8f0;
        font-size: 15px;
    }
    
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
    }
    
    .name-highlight { color: #8B0000; }
    
    .welcome-subtitle {
        font-size: 17px;
        color: #64748b;
        margin-bottom: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🔑 API Configuration")
    
    # Initialize session state for API key if not exists
    if 'api_key_stored' not in st.session_state:
        st.session_state.api_key_stored = ""
    
    # Get API key from input
    api_key_input = st.text_input(
        "Enter your OpenAI API Key",
        value=st.session_state.api_key_stored,
        type="password",
        help="Get your API key from https://platform.openai.com/api-keys",
        key="api_key_input"
    )
    
    # Store in session state
    if api_key_input:
        st.session_state.api_key_stored = api_key_input
        api_key = api_key_input
        st.success("✓ API key connected", icon="✅")
    else:
        api_key = ""
        st.warning("⚠ Please enter your API key", icon="⚠️")
    
    st.markdown("---")
    
    st.markdown("### 👤 User Settings")
    user_name = st.text_input("Your Name", value="James", key="user_name")
    user_language = st.selectbox(
        "Language",
        ["English", "Spanish", "Portuguese", "Chinese", "Japanese", "Korean", "Thai"],
        key="language"
    )
    
    st.markdown("---")
    
    st.markdown("### 📚 Knowledge Base")
    st.info("Add files to: `data/knowledge_base/`")
    
    if os.path.exists("data/knowledge_base"):
        files = glob.glob("data/knowledge_base/**/*.*", recursive=True)
        st.caption(f"📁 {len([f for f in files if os.path.isfile(f)])} files found")
    
    if st.button("🔄 Reload Knowledge Base"):
        st.cache_resource.clear()
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### ⚙️ AI Settings")
    st.caption("✓ Temperature: 0.1")
    st.caption("✓ Max Tokens: 500")
    st.caption("✓ RAG: ChromaDB")
    
    st.markdown("---")
    
    st.markdown("### 📚 Quick Links")
    st.markdown("- [Trading Guide](https://hmarkets.com/guide)")
    st.markdown("- [Support](https://hmarkets.com/support)")

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

# Initialize RAG
try:
    rag_system = get_rag_system()
except Exception as e:
    st.error(f"Failed to initialize RAG system: {e}")
    st.stop()

# MAIN CONTENT
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
                        color: white; padding: 32px; border-radius: 16px; min-height: 280px;
                        box-shadow: 0 4px 12px rgba(139, 0, 0, 0.2); display: flex;
                        flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 40px; margin-bottom: 20px;">🚀</div>
                    <div style="font-size: 24px; font-weight: 600; margin-bottom: 16px;">
                        Start Live Trading
                    </div>
                    <div style="font-size: 15px; line-height: 1.6; opacity: 0.95;">
                        Tell me your goal and account preferences — I'll set up your account to start trading
                    </div>
                </div>
                <div style="text-align: right; font-size: 32px; opacity: 0.8; margin-top: 20px;">→</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Live Trading", key="btn_start_trading", use_container_width=True):
            st.session_state.selected_option = "start_trading"
            st.session_state.conversation_started = True
            st.session_state.chat_history = [{
                "role": "assistant", 
                "content": f"Awesome, {user_name}! Let's get you started 💝\n\nBefore we begin — can you tell me how familiar you are with trading?"
            }]
            st.rerun()
    
    with col2:
        st.markdown("""
            <div style="background: white; padding: 32px; border-radius: 16px; min-height: 280px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #e2e8f0;
                        display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 40px; margin-bottom: 20px;">📚</div>
                    <div style="font-size: 24px; font-weight: 600; margin-bottom: 20px; color: #1a202c;">
                        Learn CFDs
                    </div>
                    <div style="font-size: 15px; color: #64748b; line-height: 2;">
                        📊 Master the fundamentals<br>
                        📈 Try simple examples<br>
                        📉 Level up your skills
                    </div>
                </div>
                <div style="text-align: right; font-size: 32px; color: #cbd5e0; margin-top: 20px;">→</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("📚 Learn CFDs", key="btn_learn_cfds", use_container_width=True):
            st.session_state.selected_option = "learn_cfds"
            st.session_state.conversation_started = True
            st.session_state.chat_history = [{
                "role": "assistant",
                "content": f"Great choice, {user_name}! Let's build your trading knowledge 📚\n\nWhat would you like to learn about?"
            }]
            st.rerun()
    
    with col3:
        st.markdown("""
            <div style="background: white; padding: 32px; border-radius: 16px; min-height: 280px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #e2e8f0;
                        display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 40px; margin-bottom: 20px;">💬</div>
                    <div style="font-size: 24px; font-weight: 600; margin-bottom: 16px; color: #1a202c;">
                        Take a Quick Tour
                    </div>
                    <div style="font-size: 15px; color: #64748b; line-height: 1.6;">
                        A quick walkthrough of your dashboard, features and charts
                    </div>
                </div>
                <div style="text-align: right; font-size: 32px; color: #cbd5e0; margin-top: 20px;">→</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("💬 Take a Quick Tour", key="btn_take_tour", use_container_width=True):
            st.session_state.selected_option = "take_tour"
            st.session_state.conversation_started = True
            st.session_state.chat_history = [{
                "role": "assistant",
                "content": f"Perfect, {user_name}! I'll show you around 🗺️\n\nWhat would you like to explore first?"
            }]
            st.rerun()
    
    # Chat input
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
            st.error("❌ Please enter your OpenAI API key in the sidebar", icon="🔒")
        else:
            st.session_state.last_processed_message = welcome_input
            st.session_state.conversation_started = True
            st.session_state.selected_option = "general"
            st.session_state.chat_history = [{"role": "user", "content": welcome_input}]
            st.rerun()
    
    st.markdown("""
        <div style="text-align: center; margin-top: 16px; font-size: 13px; color: #94a3b8;">
            All chats are private & encrypted. Hpulse may make mistakes — verify 
            <a href="https://hmarkets.com/risk" style="color: #3b82f6; text-decoration: none;">Key Info ↗</a>
        </div>
    """, unsafe_allow_html=True)

else:
    # ==================== CONVERSATION INTERFACE ====================
    
    thread_titles = {
        "start_trading": "Start Live Trading",
        "learn_cfds": "Learn CFDs",
        "take_tour": "Take a Quick Tour",
        "general": "Getting started!"
    }
    
    thread_title = thread_titles.get(st.session_state.selected_option, "Chat")
    
    st.markdown(f"### {thread_title}")
    
    # Display chat history
    for i, msg in enumerate(st.session_state.chat_history):
        if msg["role"] == "assistant":
            col_avatar, col_content = st.columns([1, 15])
            
            with col_avatar:
                st.markdown("""
                    <div style="width: 40px; height: 40px; background: #2d3748; border-radius: 50%; 
                                display: flex; align-items: center; justify-content: center; 
                                color: white; font-weight: 700; font-size: 16px;">H</div>
                """, unsafe_allow_html=True)
            
            with col_content:
                st.markdown(msg['content'])
                if i < len(st.session_state.chat_history) - 1:
                    st.caption("Done✅")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
        else:
            col_content, col_avatar = st.columns([15, 1])
            
            with col_content:
                st.markdown(f'<div style="text-align: right; background: #f7fafc; padding: 12px 16px; border-radius: 12px; margin-left: 60px;">{msg["content"]}</div>', unsafe_allow_html=True)
            
            with col_avatar:
                st.markdown(f"""
                    <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                                color: white; font-weight: 700; font-size: 16px;">{user_name[0]}</div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
    
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
                st.session_state.last_processed_message = user_input
                
                # Debug: Show that processing started
                st.info("Processing your message...")
                
                client = OpenAI(api_key=api_key)
                
                # RAG: Retrieve relevant knowledge
                with st.spinner("🔍 Searching your knowledge base..."):
                    retrieved_knowledge, sources = rag_system.retrieve(user_input, n_results=3)
                    st.success(f"Found {len(sources)} relevant documents")
                
                # Build user context
                user_context = {
                    'state': st.session_state.user_state,
                    'step': st.session_state.onboarding_step,
                    'language': user_language,
                    'name': user_name
                }
                
                # Build system prompt
                system_prompt = build_system_prompt(user_context, retrieved_knowledge, sources)
                
                # Add user message
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                with st.spinner("🤖 AI Mentor is thinking..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            *st.session_state.chat_history[-10:]
                        ],
                        temperature=0.1,
                        max_tokens=500
                    )
                    
                    assistant_response = response.choices[0].message.content
                    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                    st.success("Response generated!")
                
                st.rerun()
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}", icon="⚠️")
                st.error(f"Error type: {type(e).__name__}")
                import traceback
                st.code(traceback.format_exc())
    
    # Action buttons
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_clear, col_export, col_back = st.columns(3)
    
    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.conversation_started = False
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
    
    with col_back:
        if st.button("← Back", use_container_width=True):
            st.session_state.conversation_started = False
            st.rerun()

# Footer
st.markdown("---")
st.caption("""
**Risk Warning:** CFDs are complex instruments and come with a high risk of losing money rapidly due to leverage. 
Hantec Markets is licensed by FSC (Mauritius). This AI provides educational information only, not financial advice.
""")

"""
Hantec AI Mentor - RAG Implementation with ChromaDB
"""

from openai import OpenAI
import streamlit as st
import os
import glob

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Hantec AI Mentor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# RAG SYSTEM
# ============================================================================

class HantecRAG:
    def __init__(self, knowledge_base_path="data/knowledge_base"):
        """Initialize ChromaDB and load knowledge"""
        self.knowledge_base_path = knowledge_base_path
        os.makedirs(knowledge_base_path, exist_ok=True)
        
        try:
            import chromadb
            from chromadb.utils import embedding_functions
            
            self.client = chromadb.EphemeralClient()
            default_ef = embedding_functions.DefaultEmbeddingFunction()
            
            try:
                self.collection = self.client.get_collection(
                    name="hantec_knowledge",
                    embedding_function=default_ef
                )
            except:
                self.collection = self.client.create_collection(
                    name="hantec_knowledge",
                    embedding_function=default_ef,
                    metadata={"hnsw:space": "cosine"}
                )
        except Exception as e:
            st.error(f"ChromaDB initialization error: {e}")
            raise
        
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load all files from knowledge_base folder"""
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
                content = self._read_file(file_path)
                if content and len(content.strip()) > 20:
                    documents.append(content)
                    metadatas.append({
                        "source": file_path,
                        "filename": os.path.basename(file_path)
                    })
                    ids.append(file_path)
            except Exception as e:
                st.sidebar.error(f"Error loading {file_path}: {str(e)}")
        
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
        """Read file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            st.sidebar.error(f"Error reading {file_path}: {e}")
            return ""
    
    def retrieve(self, query, n_results=3):
        """Retrieve relevant documents"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            documents = results['documents'][0] if results['documents'] else []
            metadatas = results['metadatas'][0] if results['metadatas'] else []
            
            retrieved_knowledge = "\n\n".join(documents)
            sources = [m.get('filename', 'Unknown') for m in metadatas]
            
            return retrieved_knowledge, sources
        except Exception as e:
            st.sidebar.error(f"Retrieval error: {str(e)}")
            return "", []

@st.cache_resource
def get_rag_system():
    """Initialize RAG system (cached)"""
    return HantecRAG()

# ============================================================================
# AI FUNCTIONS
# ============================================================================

def build_system_prompt(user_context, retrieved_knowledge, sources):
    """Build system prompt with context"""
    source_info = f"\n\nSources: {', '.join(sources)}" if sources else ""
    
    return f"""You are the Hantec Markets AI Mentor, a conversational assistant guiding users through CFD trading.

USER CONTEXT:
- Name: {user_context.get('name', 'User')}
- State: {user_context.get('state', 'unknown')}
- Language: {user_context.get('language', 'English')}

CRITICAL CONSTRAINTS:
- NEVER mention guaranteed returns
- NO financial advice - education only
- ALWAYS include risk disclaimers for trading queries
- NEVER INVENT INFORMATION - Only use facts from knowledge base
- If knowledge base doesn't contain answer, say "I don't have specific information"

RESPONSE STRUCTURE:
- Keep answers SHORT (2-4 sentences max)
- Use bullet points for lists
- Use **bold** for emphasis
- Include ⚠️ for warnings

KNOWLEDGE BASE:
{retrieved_knowledge if retrieved_knowledge else "No specific knowledge found - MUST redirect to support."}
{source_info}

MANDATORY DISCLAIMERS:
- For trading queries: "⚠️ Trading involves risk. This is for educational purposes only."

Company: hmarkets.com | Support: support@hmarkets.com

Remember: NEVER GUESS OR INVENT INFORMATION.
"""

def get_available_topics():
    """Get list of available topics from knowledge base"""
    available_topics = []
    kb_path = "data/knowledge_base"
    
    if os.path.exists(kb_path):
        categories = [d for d in os.listdir(kb_path) 
                    if os.path.isdir(os.path.join(kb_path, d))]
        
        for category in categories:
            cat_path = os.path.join(kb_path, category)
            files = [f.replace('.txt', '').replace('.md', '').replace('_', ' ').title() 
                   for f in os.listdir(cat_path) 
                   if f.endswith(('.txt', '.md', '.json'))]
            
            if files:
                available_topics.append(f"**{category.replace('_', ' ').title()}:** {', '.join(files[:5])}")
    
    return available_topics

def process_message(user_input, api_key, rag_system, user_context):
    """Process user message and get AI response"""
    client = OpenAI(api_key=api_key)
    
    # RAG: Retrieve relevant knowledge from local files
    with st.spinner("🔍 Searching your knowledge base..."):
        retrieved_knowledge, sources = rag_system.retrieve(user_input, n_results=3)
    
    # Track all sources
    all_sources = []
    if sources:
        all_sources.extend(sources)
    
    # Check if we found relevant information
    if not retrieved_knowledge or len(retrieved_knowledge.strip()) < 50:
        # No relevant knowledge found
        available_topics = get_available_topics()
        topics_text = "\n".join([f"- {topic}" for topic in available_topics[:4]]) if available_topics else "various trading topics"
        
        response = f"I don't have specific information about that in my knowledge base.\n\n**But I can help you with:**\n{topics_text}\n\nFor other questions, please contact **support@hmarkets.com** or use our live chat (24/5).\n\nWhat would you like to know?"
        
        return response
    
    # Build system prompt and get AI response
    system_prompt = build_system_prompt(user_context, retrieved_knowledge, all_sources)
    
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
        
        ai_response = response.choices[0].message.content
        
        # Add source attribution at the bottom
        if all_sources:
            # Remove duplicates
            unique_sources = []
            seen = set()
            for s in all_sources:
                if s not in seen:
                    unique_sources.append(s)
                    seen.add(s)
            
            source_text = "\n\n---\n📚 **Source:** " + ", ".join(unique_sources)
            ai_response += source_text
        
        return ai_response
    
    # Check if we found relevant information (from files or website)
    if not retrieved_knowledge or len(retrieved_knowledge.strip()) < 50:
        # No relevant knowledge found anywhere
        available_topics = get_available_topics()
        topics_text = "\n".join([f"- {topic}" for topic in available_topics[:4]]) if available_topics else "various trading topics"
        
        response = f"I don't have specific information about that in my knowledge base.\n\n**But I can help you with:**\n{topics_text}\n\nFor other questions, please contact **support@hmarkets.com** or use our live chat (24/5).\n\nWhat would you like to know?"
        
        return response
    
    # Build system prompt and get AI response
    system_prompt = build_system_prompt(user_context, retrieved_knowledge, all_sources)
    
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
        
        ai_response = response.choices[0].message.content
        
        # Add source attribution at the bottom
        if all_sources:
            # Remove duplicates
            unique_sources = []
            seen = set()
            for s in all_sources:
                if s not in seen:
                    unique_sources.append(s)
                    seen.add(s)
            
            source_text = "\n\n---\n📚 **Source:** " + ", ".join(unique_sources)
            ai_response += source_text
        
        return ai_response

# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_message(msg, user_name):
    """Render a single chat message"""
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

def render_welcome_card(emoji, title, items, button_text, button_key, bg_color="white"):
    """Render a welcome card"""
    text_color = "white" if bg_color != "white" else "#1a202c"
    item_color = "rgba(255,255,255,0.95)" if bg_color != "white" else "#64748b"
    
    st.markdown(f"""
        <div style="background: {bg_color}; padding: 32px; border-radius: 16px; min-height: 280px;
                    box-shadow: {'0 4px 12px rgba(139, 0, 0, 0.2)' if bg_color != 'white' else '0 2px 8px rgba(0,0,0,0.08)'}; 
                    border: {'none' if bg_color != 'white' else '1px solid #e2e8f0'};
                    display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="display: flex; align-items: center; margin-bottom: 20px;">
                    <div style="font-size: 40px; margin-right: 12px;">{emoji}</div>
                    <div style="font-size: 24px; font-weight: 600; color: {text_color};">{title}</div>
                </div>
                <div style="font-size: 15px; color: {item_color}; line-height: 2;">
                    {"<br>".join(items)}
                </div>
            </div>
            <div style="text-align: right; font-size: 32px; color: {'rgba(255,255,255,0.8)' if bg_color != 'white' else '#cbd5e0'}; margin-top: 20px;">→</div>
        </div>
    """, unsafe_allow_html=True)
    
    return st.button(f"{emoji} {title}", key=button_key, use_container_width=True)

# ============================================================================
# MAIN APP
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
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🔑 API Configuration")
    
    if 'api_key_stored' not in st.session_state:
        st.session_state.api_key_stored = ""
    
    api_key_input = st.text_input(
        "Enter your OpenAI API Key",
        value=st.session_state.api_key_stored,
        type="password",
        help="Get your API key from https://platform.openai.com/api-keys",
        key="api_key_input"
    )
    
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
    if os.path.exists("data/knowledge_base"):
        files = glob.glob("data/knowledge_base/**/*.*", recursive=True)
        st.caption(f"📁 {len([f for f in files if os.path.isfile(f)])} files found")
    
    if st.button("🔄 Reload Knowledge Base"):
        st.cache_resource.clear()
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### ⚙️ AI Settings")
    st.caption("✓ Model: GPT-4o-mini")
    st.caption("✓ Temperature: 0.1")
    st.caption("✓ Max Tokens: 500")
    st.caption("✓ RAG: ChromaDB")

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
if 'message_counter' not in st.session_state:
    st.session_state.message_counter = 0

# Initialize RAG
try:
    rag_system = get_rag_system()
except Exception as e:
    st.error(f"Failed to initialize RAG system: {e}")
    st.stop()

# Main content
if not st.session_state.conversation_started:
    # ==================== WELCOME SCREEN ====================
    
    st.markdown(f"""
        <div style="text-align: center; padding: 60px 20px 50px 20px;">
            <div style="width: 90px; height: 90px; background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
                        border-radius: 50%; margin: 0 auto 25px auto; display: flex; align-items: center;
                        justify-content: center; font-size: 36px; color: white; font-weight: 700;
                        font-style: italic; box-shadow: 0 8px 16px rgba(0,0,0,0.15);">H</div>
            <div style="font-size: 36px; font-weight: 600; color: #1a202c; margin-bottom: 16px;">
                Welcome to Hantec one, <span style="color: #8B0000;">{user_name}</span> 👋
            </div>
            <div style="font-size: 18px; color: #64748b; margin-bottom: 50px;">
                Pick an option below to continue — or ask me anything to get started
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Three option cards
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        if render_welcome_card(
            "🚀", "Start Live Trading",
            ["📊 Set up your account", "💰 Make your first deposit", "🎯 Start trading CFDs"],
            "🚀 Start Live Trading", "btn_start_trading",
            "linear-gradient(135deg, #8B0000 0%, #B22222 100%)"
        ):
            st.session_state.selected_option = "start_trading"
            st.session_state.conversation_started = True
            st.session_state.chat_history = [{
                "role": "assistant", 
                "content": f"Awesome, {user_name}! Let's get you started 💝\n\nBefore we begin — can you tell me how familiar you are with trading?"
            }]
            st.rerun()
    
    with col2:
        if render_welcome_card(
            "📚", "Learn CFDs",
            ["📊 Master the fundamentals", "📈 Try simple examples", "📉 Level up your skills"],
            "📚 Learn CFDs", "btn_learn_cfds"
        ):
            st.session_state.selected_option = "learn_cfds"
            st.session_state.conversation_started = True
            st.session_state.chat_history = [{
                "role": "assistant",
                "content": f"Great choice, {user_name}! Let's build your trading knowledge 📚\n\nWhat would you like to learn about?"
            }]
            st.rerun()
    
    with col3:
        if render_welcome_card(
            "💬", "Take a Quick Tour",
            ["🗺️ Dashboard walkthrough", "📈 Features overview", "📊 Charts and tools"],
            "💬 Take a Quick Tour", "btn_take_tour"
        ):
            st.session_state.selected_option = "take_tour"
            st.session_state.conversation_started = True
            st.session_state.chat_history = [{
                "role": "assistant",
                "content": f"Perfect, {user_name}! I'll show you around 🗺️\n\nWhat would you like to explore first?"
            }]
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
            st.error("❌ Please enter your OpenAI API key in the sidebar", icon="🔒")
        else:
            try:
                st.session_state.last_processed_message = welcome_input
                st.session_state.conversation_started = True
                st.session_state.selected_option = "general"
                
                # Add user message
                st.session_state.chat_history = [{"role": "user", "content": welcome_input}]
                
                # Get AI response
                user_context = {
                    'state': st.session_state.user_state,
                    'step': st.session_state.onboarding_step,
                    'language': user_language,
                    'name': user_name
                }
                
                ai_response = process_message(welcome_input, api_key, rag_system, user_context)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                
                st.rerun()
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}", icon="⚠️")

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
    for msg in st.session_state.chat_history:
        render_message(msg, user_name)
    
    # Chat input
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_input, col_mic = st.columns([20, 1])
    
    with col_input:
        user_input = st.text_input(
            "Message",
            placeholder="Ask me anything...",
            key=f"chat_input_field_{st.session_state.message_counter}",
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
                
                # Add user message
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                # Get AI response
                user_context = {
                    'state': st.session_state.user_state,
                    'step': st.session_state.onboarding_step,
                    'language': user_language,
                    'name': user_name
                }
                
                ai_response = process_message(user_input, api_key, rag_system, user_context)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                
                # Clear input for next message
                st.session_state.message_counter += 1
                st.rerun()
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}", icon="⚠️")
    
    # Action buttons
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_back, col_clear = st.columns(2)
    
    with col_back:
        if st.button("← Back", use_container_width=True):
            st.session_state.conversation_started = False
            st.rerun()
    
    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.last_processed_message = ""
            st.rerun()

# Footer
st.markdown("---")
st.caption("""
**Risk Warning:** CFDs are complex instruments and come with a high risk of losing money rapidly due to leverage. 
Hantec Markets is licensed by FSC (Mauritius). This AI provides educational information only, not financial advice.
""")

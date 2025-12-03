"""
Hantec AI Mentor - Conversational Flow System
Hybrid Approach: Decision Tree + LLM Enhancement
"""

from openai import OpenAI
import streamlit as st

# ============================================================================
# CONVERSATION STATE MANAGEMENT
# ============================================================================

class ConversationState:
    """Manage user profile and conversation state"""
    
    def __init__(self):
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = {
                'age_range': None,
                'trading_experience': None,
                'traded_before': None,
                'familiar_with_cfds': None,
                'investment_goal': None,
                'risk_tolerance': None,
                'monthly_investment': None,
                'onboarding_step': None,
                'conversation_path': None,  # beginner/intermediate/advanced
                'profiling_complete': False
            }
        
        if 'conversation_stage' not in st.session_state:
            st.session_state.conversation_stage = 'age'  # Current question stage
        
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []
    
    def update_profile(self, key, value):
        """Update user profile"""
        st.session_state.user_profile[key] = value
    
    def get_profile(self):
        """Get current profile"""
        return st.session_state.user_profile
    
    def is_profiling_complete(self):
        """Check if profiling questions are complete"""
        profile = st.session_state.user_profile
        required_fields = [
            'age_range', 'trading_experience', 'traded_before',
            'familiar_with_cfds', 'investment_goal', 'risk_tolerance',
            'monthly_investment', 'onboarding_step'
        ]
        return all(profile.get(field) is not None for field in required_fields)

# ============================================================================
# DECISION TREE - PROFILING QUESTIONS
# ============================================================================

class ProfilingQuestions:
    """Decision tree for structured profiling questions"""
    
    QUESTIONS = {
        'age': {
            'question': "Great! Let's get you started 🚀\n\nFirst, what's your age range?",
            'options': ['18-22', '22-30', '30-40', '40-50', '50+'],
            'next_stage': 'trading_experience'
        },
        'trading_experience': {
            'question': "Perfect! How much trading experience do you have?",
            'options': ['Complete Beginner', 'Some Knowledge', 'Experienced'],
            'next_stage': 'traded_before'
        },
        'traded_before': {
            'question': "Have you ever traded before?",
            'options': ['Yes', 'No'],
            'next_stage': 'familiar_with_cfds'
        },
        'familiar_with_cfds': {
            'question': "Are you familiar with CFDs (Contracts for Difference)?",
            'options': ['Yes', 'No'],
            'next_stage': 'investment_goal'
        },
        'investment_goal': {
            'question': "What's your main investment goal?",
            'options': ['Short-term', 'Long-term', 'Both'],
            'next_stage': 'risk_tolerance'
        },
        'risk_tolerance': {
            'question': "What's your risk tolerance?",
            'options': ['Low', 'Medium', 'High'],
            'next_stage': 'monthly_investment'
        },
        'monthly_investment': {
            'question': "What's your expected monthly investment?",
            'options': ['10-20k', '20k+'],
            'next_stage': 'onboarding_step'
        },
        'onboarding_step': {
            'question': "Let me check where you are in the account setup. Which step have you completed?",
            'options': [
                '1. Account created',
                '2. Registration filled',
                '3. Email verified',
                '4. KYC - ID uploaded',
                '5. KYC - Address uploaded',
                '6. ID approved',
                '7. Address approved',
                '8. First deposit made',
                '9. Ready to trade'
            ],
            'next_stage': 'profiling_complete'
        }
    }
    
    @staticmethod
    def get_question(stage):
        """Get question for current stage"""
        return ProfilingQuestions.QUESTIONS.get(stage, {})
    
    @staticmethod
    def get_next_stage(current_stage):
        """Get next stage in conversation"""
        question_data = ProfilingQuestions.QUESTIONS.get(current_stage, {})
        return question_data.get('next_stage')

# ============================================================================
# CONVERSATION PATHS - DECISION TREE LOGIC
# ============================================================================

class ConversationPaths:
    """Define conversation paths based on user profile"""
    
    @staticmethod
    def determine_path(profile):
        """Determine which conversation path to follow"""
        experience = profile.get('trading_experience', '').lower()
        
        if 'beginner' in experience:
            return 'beginner'
        elif 'knowledge' in experience:
            return 'intermediate'
        elif 'experienced' in experience:
            return 'advanced'
        return 'beginner'  # Default
    
    @staticmethod
    def get_learning_plan(profile):
        """Get comprehensive learning plan based on experience level"""
        path = ConversationPaths.determine_path(profile)
        risk = profile.get('risk_tolerance', 'Medium').lower()
        goal = profile.get('investment_goal', 'Both').lower()
        
        learning_plans = {
            'beginner': {
                'title': '🎓 Your Personalized Learning Journey',
                'duration': '2-4 weeks',
                'modules': [
                    {
                        'week': 'Week 1: Foundations',
                        'topics': [
                            '📖 What are CFDs? (Contract for Difference)',
                            '💰 Understanding leverage and margin',
                            '📊 How to read price charts',
                            '🎯 Basic trading terminology',
                            '⚠️ Risk management basics'
                        ],
                        'time': '30 minutes/day',
                        'action': '[Start Week 1 →](https://hmarkets.com/education/basics)'
                    },
                    {
                        'week': 'Week 2: Platform Training',
                        'topics': [
                            '💻 MT4/MT5 platform walkthrough',
                            '📱 Mobile app features',
                            '📈 Placing your first order (demo)',
                            '🛡️ Setting stop-loss & take-profit',
                            '📊 Understanding order types'
                        ],
                        'time': '45 minutes/day',
                        'action': '[Open Demo Account →](https://hmarkets.com/demo)'
                    },
                    {
                        'week': 'Week 3: Strategy & Practice',
                        'topics': [
                            '📊 Technical analysis basics',
                            '📰 Fundamental analysis intro',
                            '🎯 Simple trading strategies',
                            '💡 Practice with demo account',
                            '📝 Keeping a trading journal'
                        ],
                        'time': '1 hour/day',
                        'action': '[Practice Strategies →](https://hmarkets.com/education/strategies)'
                    },
                    {
                        'week': 'Week 4: Going Live',
                        'topics': [
                            '💰 Making your first deposit',
                            '🎯 Starting with small positions',
                            '📊 Your first real trade',
                            '🛡️ Risk management in practice',
                            '📈 Tracking your progress'
                        ],
                        'time': 'Start small',
                        'action': '[Fund Account →](https://hmarkets.com/deposit)'
                    }
                ],
                'resources': [
                    '📚 [Trading Glossary](https://hmarkets.com/glossary)',
                    '🎥 [Video Tutorials](https://hmarkets.com/videos)',
                    '💬 [Community Forum](https://hmarkets.com/community)',
                    '📧 [Weekly Newsletter](https://hmarkets.com/newsletter)'
                ],
                'tips': [
                    '💡 Start with demo account - practice until confident',
                    '⚠️ Never risk more than 1-2% of capital per trade',
                    '📊 Focus on learning, not just profit',
                    '🎯 Set realistic expectations - trading is a skill'
                ]
            },
            'intermediate': {
                'title': '🚀 Accelerated Trading Program',
                'duration': '1-2 weeks',
                'modules': [
                    {
                        'week': 'Days 1-3: Platform Mastery',
                        'topics': [
                            '💻 Hantec platform features',
                            '📊 Advanced order types',
                            '🛡️ Risk management tools',
                            '📱 Trading on mobile',
                            '🔔 Setting up alerts'
                        ],
                        'time': '2-3 hours',
                        'action': '[Platform Guide →](https://hmarkets.com/platforms)'
                    },
                    {
                        'week': 'Days 4-7: Strategy Refinement',
                        'topics': [
                            '📈 Technical indicators deep dive',
                            '📊 Chart patterns recognition',
                            '🎯 Backtesting strategies',
                            '💡 Position sizing',
                            '📝 Trade planning'
                        ],
                        'time': '3-4 hours',
                        'action': '[Advanced Strategies →](https://hmarkets.com/education/advanced)'
                    },
                    {
                        'week': 'Week 2: Live Trading',
                        'topics': [
                            '💰 Fund your account',
                            '🎯 Start with tested strategies',
                            '📊 Monitor and adjust',
                            '📈 Scale gradually',
                            '🛡️ Refine risk management'
                        ],
                        'time': 'Active trading',
                        'action': '[Start Trading →](https://hmarkets.com/trading-platform)'
                    }
                ],
                'resources': [
                    '📊 [Market Analysis](https://hmarkets.com/tools/market-analysis)',
                    '🔔 [Trading Signals](https://hmarkets.com/signals)',
                    '📈 [Economic Calendar](https://hmarkets.com/calendar)',
                    '💬 [Trading Community](https://hmarkets.com/community)'
                ],
                'tips': [
                    '💡 Review your past trades - learn from mistakes',
                    '⚠️ Don\'t overtrade - quality over quantity',
                    '📊 Use stop losses on every trade',
                    '🎯 Keep emotions in check - stick to your plan'
                ]
            },
            'advanced': {
                'title': '⚡ Advanced Trader Setup',
                'duration': '2-3 days',
                'modules': [
                    {
                        'week': 'Day 1: Account Setup',
                        'topics': [
                            '⚡ Complete verification quickly',
                            '💰 Fund your account',
                            '🔧 Configure platform settings',
                            '📊 Set up charts & indicators',
                            '🔔 Custom alerts & notifications'
                        ],
                        'time': '1-2 hours',
                        'action': '[Account Setup →](https://hmarkets.com/account)'
                    },
                    {
                        'week': 'Day 2-3: Advanced Features',
                        'topics': [
                            '🤖 Algorithmic trading setup',
                            '📊 Advanced charting tools',
                            '🔍 Market depth & liquidity',
                            '💡 Copy trading features',
                            '📈 Portfolio management tools'
                        ],
                        'time': '2-3 hours',
                        'action': '[Advanced Tools →](https://hmarkets.com/tools/advanced)'
                    }
                ],
                'resources': [
                    '🤖 [Algo Trading](https://hmarkets.com/algo-trading)',
                    '📊 [InsightPro Analysis](https://hmarkets.com/tools/market-analysis)',
                    '💼 [Portfolio Tools](https://hmarkets.com/portfolio)',
                    '📱 [API Documentation](https://hmarkets.com/api)'
                ],
                'tips': [
                    '💡 Leverage your experience but respect new platform',
                    '⚠️ Test strategies with small positions first',
                    '📊 Explore Hantec\'s unique features',
                    '🎯 Connect with account manager for VIP features'
                ]
            }
        }
        
        return learning_plans.get(path, learning_plans['beginner'])
    
    @staticmethod
    def get_path_greeting(profile):
        """Get personalized greeting based on path"""
        path = ConversationPaths.determine_path(profile)
        age = profile.get('age_range', '')
        goal = profile.get('investment_goal', '').lower()
        
        greetings = {
            'beginner': f"""
Awesome! 🎯 Let me create a personalized roadmap for you.

**Your Profile:**
- Age: {age}
- Experience: Beginner
- Goal: {goal.title()}

Since you're new to trading, here's your path to success:

📚 **Step 1:** Learn the basics (5-10 minutes)
💰 **Step 2:** Open a demo account (practice with virtual money)
📊 **Step 3:** Start with small real trades

Ready to begin?
""",
            'intermediate': f"""
Great! 🚀 You have some knowledge - let's fast-track you!

**Your Profile:**
- Age: {age}
- Experience: Intermediate
- Goal: {goal.title()}

Here's your streamlined path:

✅ **Step 1:** Quick platform overview (3 minutes)
💰 **Step 2:** Complete account setup
📊 **Step 3:** Fund & start trading

Let's get you trading quickly!
""",
            'advanced': f"""
Perfect! ⚡ Let's get you set up fast.

**Your Profile:**
- Age: {age}
- Experience: Advanced
- Goal: {goal.title()}

Express setup for experienced traders:

⚡ **Step 1:** Account verification
💰 **Step 2:** Fund your account
📊 **Step 3:** Access advanced features

Ready to trade?
"""
        }
        
        return greetings.get(path, greetings['beginner'])
    
    @staticmethod
    def get_next_action(profile):
        """Determine next action based on onboarding step"""
        step = profile.get('onboarding_step', '')
        
        actions = {
            '1. Account created': {
                'title': 'Complete Registration',
                'description': 'Fill out your registration form (2 minutes)',
                'why': 'We need your basic information to comply with regulations.',
                'time': '2 minutes',
                'link': 'https://hmarkets.com/register'
            },
            '2. Registration filled': {
                'title': 'Verify Email',
                'description': 'Check your inbox and click the verification link',
                'why': 'To confirm your email address and secure your account.',
                'time': '1 minute',
                'link': 'https://hmarkets.com/verify-email'
            },
            '3. Email verified': {
                'title': 'Upload ID',
                'description': 'Upload a photo of your ID (Passport, Driver\'s License, or National ID)',
                'why': 'Required by regulation to verify your identity and protect you.',
                'time': '2 minutes',
                'link': 'https://hmarkets.com/kyc/upload-id'
            },
            '4. KYC - ID uploaded': {
                'title': 'Upload Address Proof',
                'description': 'Upload a recent utility bill or bank statement',
                'why': 'To verify your residential address as required by regulation.',
                'time': '2 minutes',
                'link': 'https://hmarkets.com/kyc/upload-address'
            },
            '5. KYC - Address uploaded': {
                'title': 'Wait for Approval',
                'description': 'Your documents are being reviewed',
                'why': 'We need to verify your identity to comply with regulations.',
                'time': '24-48 hours',
                'link': None
            },
            '6. ID approved': {
                'title': 'Wait for Address Approval',
                'description': 'Your address document is being reviewed',
                'why': 'Final step in identity verification process.',
                'time': '24-48 hours',
                'link': None
            },
            '7. Address approved': {
                'title': 'Make First Deposit',
                'description': 'Fund your account to start trading',
                'why': 'You need capital to trade. Start small if you\'re new!',
                'time': '5 minutes',
                'link': 'https://hmarkets.com/deposit'
            },
            '8. First deposit made': {
                'title': 'Try Demo Account',
                'description': 'Practice with virtual money before risking real funds',
                'why': 'Build confidence and learn the platform risk-free.',
                'time': '10-30 minutes',
                'link': 'https://hmarkets.com/demo'
            },
            '9. Ready to trade': {
                'title': 'Place Your First Trade',
                'description': 'You\'re all set! Start trading.',
                'why': 'Everything is ready - time to take action!',
                'time': 'Now!',
                'link': 'https://hmarkets.com/trading-platform'
            }
        }
        
        return actions.get(step, actions['1. Account created'])

# ============================================================================
# LLM ENHANCEMENT
# ============================================================================

class LLMEnhancement:
    """Use LLM for natural responses and clarifications"""
    
    @staticmethod
    def generate_personalized_response(profile, user_query, api_key):
        """Generate personalized response using LLM"""
        
        # Build context from profile
        context = f"""
User Profile:
- Age Range: {profile.get('age_range', 'Unknown')}
- Trading Experience: {profile.get('trading_experience', 'Unknown')}
- Traded Before: {profile.get('traded_before', 'Unknown')}
- Familiar with CFDs: {profile.get('familiar_with_cfds', 'Unknown')}
- Investment Goal: {profile.get('investment_goal', 'Unknown')}
- Risk Tolerance: {profile.get('risk_tolerance', 'Unknown')}
- Monthly Investment: {profile.get('monthly_investment', 'Unknown')}
- Onboarding Step: {profile.get('onboarding_step', 'Unknown')}
- Conversation Path: {profile.get('conversation_path', 'Unknown')}

User Question: {user_query}
"""
        
        system_prompt = """You are Hantec Markets AI Mentor, helping users start their trading journey.

PERSONALITY:
- Encouraging and motivational
- Clear and concise
- Patient with beginners
- Professional but friendly

GUIDELINES:
- Keep responses SHORT (2-4 sentences)
- Use emojis sparingly 🎯 💰 📊
- Always end with a clear next step or question
- For beginners: Be educational
- For experienced: Be efficient
- Include risk disclaimers when discussing trading

CRITICAL:
- NEVER give financial advice
- NEVER guarantee returns
- ALWAYS emphasize that trading involves risk
- If unsure, redirect to support@hmarkets.com

Respond naturally to the user's question based on their profile.
"""
        
        try:
            client = OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context}
                ],
                temperature=0.7,  # Slightly higher for more natural conversation
                max_tokens=300
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"I'm having trouble right now. Please contact support@hmarkets.com or try again. Error: {str(e)}"
    
    @staticmethod
    def generate_motivational_tip(profile, api_key):
        """Generate personalized motivational tip"""
        
        path = profile.get('conversation_path', 'beginner')
        
        tips_context = f"""
Generate a SHORT (1-2 sentences) motivational trading tip for a {path} trader.

Make it:
- Encouraging
- Actionable
- Relevant to their experience level

Start with 💡 **Tip:**
"""
        
        try:
            client = OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You generate short, actionable trading tips."},
                    {"role": "user", "content": tips_context}
                ],
                temperature=0.8,
                max_tokens=100
            )
            
            return response.choices[0].message.content
        
        except:
            return "💡 **Tip:** Start small, learn continuously, and never risk more than you can afford to lose!"

# ============================================================================
# CONVERSATION FLOW MANAGER
# ============================================================================

class ConversationFlowManager:
    """Orchestrate the conversation flow"""
    
    def __init__(self, api_key):
        self.state = ConversationState()
        self.api_key = api_key
    
    def render_profiling_question(self):
        """Render current profiling question with buttons"""
        stage = st.session_state.conversation_stage
        
        if stage == 'profiling_complete':
            self.render_path_summary()
            return
        
        question_data = ProfilingQuestions.get_question(stage)
        
        if not question_data:
            return
        
        # Display question
        st.markdown(question_data['question'])
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display button options
        cols = st.columns(len(question_data['options']))
        
        for idx, option in enumerate(question_data['options']):
            with cols[idx]:
                if st.button(option, key=f"btn_{stage}_{idx}", use_container_width=True):
                    # Store answer
                    self.state.update_profile(stage, option)
                    
                    # Move to next stage
                    next_stage = question_data['next_stage']
                    st.session_state.conversation_stage = next_stage
                    
                    # Add to conversation history
                    st.session_state.conversation_history.append({
                        'role': 'user',
                        'content': option
                    })
                    
                    st.rerun()
    
    def render_path_summary(self):
        """Render personalized learning plan after profiling"""
        profile = self.state.get_profile()
        
        # Determine path
        path = ConversationPaths.determine_path(profile)
        self.state.update_profile('conversation_path', path)
        self.state.update_profile('profiling_complete', True)
        
        # Show profile summary
        st.markdown("## ✅ Profile Complete!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Experience", profile.get('trading_experience', 'N/A'))
        with col2:
            st.metric("Goal", profile.get('investment_goal', 'N/A'))
        with col3:
            st.metric("Risk Tolerance", profile.get('risk_tolerance', 'N/A'))
        
        st.markdown("---")
        
        # Get and display learning plan
        learning_plan = ConversationPaths.get_learning_plan(profile)
        
        st.markdown(f"## {learning_plan['title']}")
        st.markdown(f"**⏱️ Estimated Duration:** {learning_plan['duration']}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display learning modules
        for idx, module in enumerate(learning_plan['modules'], 1):
            with st.expander(f"📖 {module['week']}", expanded=(idx==1)):
                st.markdown(f"**⏰ Time Commitment:** {module['time']}")
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown("**📚 What You'll Learn:**")
                for topic in module['topics']:
                    st.markdown(f"- {topic}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(module['action'])
        
        st.markdown("---")
        
        # Learning resources
        st.markdown("### 📚 Learning Resources")
        cols = st.columns(2)
        for idx, resource in enumerate(learning_plan['resources']):
            with cols[idx % 2]:
                st.markdown(resource)
        
        st.markdown("---")
        
        # Pro tips
        st.markdown("### 💡 Pro Tips for Success")
        for tip in learning_plan['tips']:
            st.markdown(tip)
        
        st.markdown("---")
        
        # Current onboarding status & next action
        st.markdown("## 🎯 Your Next Immediate Action")
        
        next_action = ConversationPaths.get_next_action(profile)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {next_action['title']}")
            st.markdown(f"**What:** {next_action['description']}")
            st.markdown(f"**Why:** {next_action['why']}")
            st.markdown(f"**Time:** {next_action['time']}")
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if next_action['link']:
                st.link_button(f"✅ {next_action['title']}", next_action['link'], use_container_width=True)
            else:
                st.info("⏳ Waiting for approval")
        
        st.markdown("---")
        
        # Allow free-text questions
        st.markdown("### 💬 Have Questions About Your Learning Path?")
        
        user_question = st.text_input(
            "Ask me anything...",
            key="free_text_question",
            placeholder="e.g., Can I skip the demo account? or How much should I start with?"
        )
        
        if user_question:
            with st.spinner("🤔 Thinking..."):
                if self.api_key:
                    response = LLMEnhancement.generate_personalized_response(
                        profile,
                        user_question,
                        self.api_key
                    )
                    st.markdown(response)
                else:
                    st.error("Please enter API key in sidebar to ask questions")

# ============================================================================
# MAIN CONVERSATION INTERFACE
# ============================================================================

def render_conversation_flow(api_key):
    """Main function to render conversation flow"""
    
    # Initialize flow manager
    flow_manager = ConversationFlowManager(api_key)
    
    # Check if profiling is complete
    if st.session_state.user_profile.get('profiling_complete'):
        flow_manager.render_path_summary()
    else:
        flow_manager.render_profiling_question()
    
    # Show progress indicator
    render_progress_indicator()

def render_progress_indicator():
    """Show user where they are in the profiling process"""
    total_questions = 8  # Total profiling questions
    
    # Map stages to question numbers
    stage_numbers = {
        'age': 1,
        'trading_experience': 2,
        'traded_before': 3,
        'familiar_with_cfds': 4,
        'investment_goal': 5,
        'risk_tolerance': 6,
        'monthly_investment': 7,
        'onboarding_step': 8,
        'profiling_complete': 8
    }
    
    current_stage = st.session_state.conversation_stage
    current_number = stage_numbers.get(current_stage, 1)
    
    progress = current_number / total_questions
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(progress)
    st.caption(f"Question {current_number} of {total_questions}")

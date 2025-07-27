import streamlit as st
import sys
import os
from conversation_crew import ConversationCrew
import time
import json
import re
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="NSE Stock Analysis Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for chat-like interface
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    .stDeployButton {display: none;}
    .stDecoration {display: none;}
    #MainMenu {visibility: hidden;}
    .stAppHeader {display: none;}
    
    /* Chat container styling */
    .chat-container {
        max-width: 100%;
        margin: 0 auto;
        padding: 20px;
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    /* Header styling */
    .chat-header {
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 16px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .chat-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .chat-header p {
        margin: 10px 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Message styling */
    .message {
        display: flex;
        margin-bottom: 20px;
        animation: slideIn 0.3s ease-out;
    }
    
    .user-message {
        justify-content: flex-end;
    }
    
    .assistant-message {
        justify-content: flex-start;
    }
    
    .message-content {
        max-width: 70%;
        padding: 16px 20px;
        border-radius: 20px;
        font-size: 16px;
        line-height: 1.5;
        word-wrap: break-word;
    }
    
    .user-message .message-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 6px;
    }
    
    .assistant-message .message-content {
        background: #f7f7f8;
        color: #1a1a1a;
        border: 1px solid #e5e5e5;
        border-bottom-left-radius: 6px;
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 12px;
        font-size: 20px;
        font-weight: bold;
        flex-shrink: 0;
    }
    
    .user-avatar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        order: 1;
    }
    
    .assistant-avatar {
        background: #f0f0f0;
        color: #666;
        order: 0;
    }
    
    /* Suggestions styling */
    .suggestions {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 20px 0;
        justify-content: center;
    }
    
    .suggestion-chip {
        background: #f7f7f8;
        border: 1px solid #e5e5e5;
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .suggestion-chip:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 20px 0;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #667eea;
        animation: typing 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-20px); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Stock data styling */
    .stock-data {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    }
    
    .stock-metric {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .stock-metric:last-child {
        border-bottom: none;
    }
    
    .metric-label {
        font-weight: 600;
        color: #4a5568;
    }
    
    .metric-value {
        font-weight: 700;
        color: #1a202c;
    }
    
    .metric-positive {
        color: #22c55e;
    }
    
    .metric-negative {
        color: #ef4444;
    }
    
    /* Chat messages area */
    .chat-messages {
        min-height: 60vh;
        max-height: 70vh;
        overflow-y: auto;
        padding-bottom: 20px;
    }
    
    /* Scrollbar styling */
    .chat-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 3px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    
    /* Sidebar styling */
    .sidebar-content {
        padding: 1rem;
    }
    
    .api-status {
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: 600;
    }
    
    .api-status.connected {
        background: #dcfce7;
        color: #166534;
        border: 1px solid #bbf7d0;
    }
    
    .api-status.disconnected {
        background: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
    }
    
    .api-key-section {
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    .api-key-label {
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .api-key-preview {
        font-size: 0.8rem;
        color: #6b7280;
        margin-bottom: 0.5rem;
        font-family: monospace;
        background: #f3f4f6;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
    }
    
    .welcome-message {
        text-align: center;
        padding: 2rem;
        background: #f8fafc;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    
    .welcome-message h3 {
        margin-bottom: 1rem;
        color: #1a202c;
    }
    
    .welcome-message p {
        color: #4a5568;
        line-height: 1.6;
    }
    
    /* Input area styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e5e5e5;
        padding: 12px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'crew' not in st.session_state:
    st.session_state.crew = None
if 'is_typing' not in st.session_state:
    st.session_state.is_typing = False
if 'api_keys_set' not in st.session_state:
    st.session_state.api_keys_set = False

# Default API keys (can be overridden by user)
DEFAULT_API_KEYS = {
    'GEMINI_API_KEY': 'AIzaSyAIozB0ryxa5bEua2-RCPsav1zVPuMejZw',
    'SERPER_API_KEY': 'c1ef6e40d489b6728585aebcc6b832a7384627a1',
    'INDIAN_API_KEY': 'sk-live-efd6p1wyz4wDUWtKAGLzn4diji8ObRXgPC4d05Ir'
}

def set_api_keys():
    """Set API keys in environment variables"""
    for key, value in DEFAULT_API_KEYS.items():
        if key not in os.environ or not os.environ[key]:
            os.environ[key] = value
    st.session_state.api_keys_set = True

def update_api_keys(gemini_key, serper_key, indian_key):
    """Update API keys with user provided values"""
    updated = False
    
    if gemini_key and gemini_key.strip():
        os.environ['GEMINI_API_KEY'] = gemini_key.strip()
        DEFAULT_API_KEYS['GEMINI_API_KEY'] = gemini_key.strip()
        updated = True
    
    if serper_key and serper_key.strip():
        os.environ['SERPER_API_KEY'] = serper_key.strip()
        DEFAULT_API_KEYS['SERPER_API_KEY'] = serper_key.strip()
        updated = True
    
    if indian_key and indian_key.strip():
        os.environ['INDIAN_API_KEY'] = indian_key.strip()
        DEFAULT_API_KEYS['INDIAN_API_KEY'] = indian_key.strip()
        updated = True
    
    if updated:
        # Reset crew to use new API keys
        st.session_state.crew = None
        st.session_state.api_keys_set = True
        return True
    return False

def initialize_crew():
    """Initialize the conversation crew"""
    try:
        # Ensure API keys are set
        set_api_keys()
        
        if st.session_state.crew is None:
            st.session_state.crew = ConversationCrew()
        return True
    except Exception as e:
        st.error(f"Failed to initialize system: {str(e)}")
        return False

def parse_json_response(response_text):
    """Parse JSON from response and format it nicely"""
    try:
        # Look for JSON content within ```json blocks
        json_pattern = r'```json\s*({.*?})\s*```'
        match = re.search(json_pattern, response_text, re.DOTALL)
        
        if match:
            json_str = match.group(1)
            data = json.loads(json_str)
            
            # Format the insights nicely
            formatted_response = ""
            
            if 'insights' in data:
                formatted_response += data['insights']
            
            # Add additional structured data if available
            if 'additional_info' in data:
                additional_info = data['additional_info']
                
                # Add market data
                if 'market_data' in additional_info:
                    market_data = additional_info['market_data']
                    formatted_response += "\n\n📊 **Market Data:**"
                    
                    stock_html = '<div class="stock-data">'
                    
                    if 'current_price_nse' in market_data:
                        stock_html += f'<div class="stock-metric"><span class="metric-label">NSE Price</span><span class="metric-value">₹{market_data["current_price_nse"]}</span></div>'
                    
                    if 'current_price_bse' in market_data:
                        stock_html += f'<div class="stock-metric"><span class="metric-label">BSE Price</span><span class="metric-value">₹{market_data["current_price_bse"]}</span></div>'
                    
                    if 'daily_change' in market_data:
                        change = market_data['daily_change']
                        change_class = 'metric-positive' if not change.startswith('-') else 'metric-negative'
                        stock_html += f'<div class="stock-metric"><span class="metric-label">Daily Change</span><span class="metric-value {change_class}">{change}</span></div>'
                    
                    if '52_week_high' in market_data:
                        stock_html += f'<div class="stock-metric"><span class="metric-label">52W High</span><span class="metric-value">₹{market_data["52_week_high"]}</span></div>'
                    
                    if '52_week_low' in market_data:
                        stock_html += f'<div class="stock-metric"><span class="metric-label">52W Low</span><span class="metric-value">₹{market_data["52_week_low"]}</span></div>'
                    
                    stock_html += '</div>'
                    
                    return formatted_response, stock_html
            
            return formatted_response, None
        
        # If no JSON found, return original response
        return response_text, None
    
    except Exception as e:
        return response_text, None

def display_message(message, is_user=True):
    """Display a chat message"""
    message_class = "user-message" if is_user else "assistant-message"
    avatar_class = "user-avatar" if is_user else "assistant-avatar"
    avatar_icon = "👤" if is_user else "🤖"
    
    # Parse message if it's from assistant
    if not is_user and isinstance(message, str):
        formatted_text, stock_html = parse_json_response(message)
        message_content = formatted_text
    else:
        message_content = message
        stock_html = None
    
    st.markdown(f"""
    <div class="message {message_class}">
        <div class="message-avatar {avatar_class}">
            {avatar_icon}
        </div>
        <div class="message-content">
            {message_content}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display stock data if available
    if stock_html:
        st.markdown(stock_html, unsafe_allow_html=True)

def display_typing_indicator():
    """Display typing indicator"""
    st.markdown("""
    <div class="message assistant-message">
        <div class="message-avatar assistant-avatar">
            🤖
        </div>
        <div class="message-content">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <span style="margin-left: 8px;">AI is analyzing...</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_ai_response(question):
    """Get response from AI crew"""
    try:
        if not st.session_state.crew:
            initialize_crew()
        
        result = st.session_state.crew.crew().kickoff(inputs={'user_question': question})
        
        # Extract response text
        if hasattr(result, 'raw'):
            return result.raw
        else:
            return str(result)
    
    except Exception as e:
        return f"I apologize, but I encountered an error while processing your request: {str(e)}"

def render_sidebar():
    """Render the sidebar with API settings"""
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        # Title
        st.title("🔧 API Settings")
        
        # API Status
        api_status = "connected" if st.session_state.api_keys_set else "disconnected"
        status_text = "✅ API Keys Active" if st.session_state.api_keys_set else "❌ API Keys Not Set"
        
        st.markdown(f"""
        <div class="api-status {api_status}">
            {status_text}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # API Key sections
        st.subheader("🔑 Configure API Keys")
        
        # Gemini API Key
        with st.expander("🧠 Google Gemini API", expanded=False):
            current_gemini = os.environ.get('GEMINI_API_KEY', '')
            if current_gemini:
                gemini_preview = f"{current_gemini[:8]}...{current_gemini[-8:]}"
                st.markdown(f'<div class="api-key-preview">Current: {gemini_preview}</div>', 
                          unsafe_allow_html=True)
            else:
                st.markdown('<div class="api-key-preview">Not configured</div>', 
                          unsafe_allow_html=True)
            
            gemini_key = st.text_input(
                "Enter Gemini API Key",
                type="password",
                placeholder="AIzaSy...",
                key="gemini_input",
                help="Get your API key from https://makersuite.google.com/app/apikey"
            )
            
            if st.button("Update Gemini Key", key="update_gemini", use_container_width=True):
                if gemini_key:
                    if update_api_keys(gemini_key, None, None):
                        st.success("✅ Gemini API key updated!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to update API key")
                else:
                    st.warning("⚠️ Please enter a valid API key")
        
        # Serper API Key
        with st.expander("🔍 Serper Search API", expanded=False):
            current_serper = os.environ.get('SERPER_API_KEY', '')
            if current_serper:
                serper_preview = f"{current_serper[:8]}...{current_serper[-8:]}"
                st.markdown(f'<div class="api-key-preview">Current: {serper_preview}</div>', 
                          unsafe_allow_html=True)
            else:
                st.markdown('<div class="api-key-preview">Not configured</div>', 
                          unsafe_allow_html=True)
            
            serper_key = st.text_input(
                "Enter Serper API Key",
                type="password",
                placeholder="c1ef6e40d489...",
                key="serper_input",
                help="Get your API key from https://serper.dev"
            )
            
            if st.button("Update Serper Key", key="update_serper", use_container_width=True):
                if serper_key:
                    if update_api_keys(None, serper_key, None):
                        st.success("✅ Serper API key updated!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to update API key")
                else:
                    st.warning("⚠️ Please enter a valid API key")
        
        # Indian Stock API Key
        with st.expander("📈 Indian Stock API", expanded=False):
            current_indian = os.environ.get('INDIAN_API_KEY', '')
            if current_indian:
                indian_preview = f"{current_indian[:8]}...{current_indian[-8:]}"
                st.markdown(f'<div class="api-key-preview">Current: {indian_preview}</div>', 
                          unsafe_allow_html=True)
            else:
                st.markdown('<div class="api-key-preview">Not configured</div>', 
                          unsafe_allow_html=True)
            
            indian_key = st.text_input(
                "Enter Indian Stock API Key",
                type="password",
                placeholder="sk-live-efd6p1wyz4w...",
                key="indian_input",
                help="Get your API key from your stock data provider"
            )
            
            if st.button("Update Indian API Key", key="update_indian", use_container_width=True):
                if indian_key:
                    if update_api_keys(None, None, indian_key):
                        st.success("✅ Indian API key updated!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to update API key")
                else:
                    st.warning("⚠️ Please enter a valid API key")
        
        st.markdown("---")
        
        # Bulk update section
        st.subheader("🔄 Bulk Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Reset All", use_container_width=True, 
                        help="Reset to default API keys"):
                update_api_keys(
                    DEFAULT_API_KEYS['GEMINI_API_KEY'],
                    DEFAULT_API_KEYS['SERPER_API_KEY'],
                    DEFAULT_API_KEYS['INDIAN_API_KEY']
                )
                st.success("✅ Reset to defaults!")
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear All", use_container_width=True, 
                        help="Clear all API keys"):
                for key in DEFAULT_API_KEYS.keys():
                    if key in os.environ:
                        del os.environ[key]
                st.session_state.api_keys_set = False
                st.session_state.crew = None
                st.warning("⚠️ All API keys cleared!")
                st.rerun()
        
        st.markdown("---")
        
        # Chat controls
        st.subheader("💬 Chat Controls")
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.session_state.is_typing = False
            st.success("✅ Chat history cleared!")
            st.rerun()
        
        # System info
        st.markdown("---")
        st.markdown("### 📊 System Status")
        
        # Check if crew is initialized
        crew_status = "✅ Ready" if st.session_state.crew else "❌ Not Initialized"
        st.markdown(f"**AI System:** {crew_status}")
        
        # Message count
        message_count = len(st.session_state.messages)
        st.markdown(f"**Messages:** {message_count}")
        
        # Typing status
        typing_status = "🔄 Processing..." if st.session_state.is_typing else "💤 Idle"
        st.markdown(f"**Status:** {typing_status}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Initialize API keys on startup
    set_api_keys()
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    with st.container():
        # Header
        st.markdown("""
        <div class="chat-header">
            <h1>💬 NSE Stock Chat</h1>
            <p>Your AI-powered stock market analysis assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize system
        if not st.session_state.crew:
            with st.spinner("🔄 Initializing AI system..."):
                initialize_crew()
        
        # Chat messages container
        st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
        
        # Display welcome message if no messages
        if not st.session_state.messages:
            st.markdown("""
            <div class="welcome-message">
                <h3>👋 Welcome to NSE Stock Chat!</h3>
                <p>I'm here to help you with Indian stock market analysis. Ask me anything about stocks, IPOs, market data, or companies listed on NSE/BSE.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Suggestion chips
            suggestions = [
                "Current price of TCS",
                "Reliance stock analysis",
                "Today's top gainers",
                "HDFC Bank performance",
                "Recent IPO listings",
                "Nifty 50 overview"
            ]
            
            st.markdown("### 💡 Try asking about:")
            
            cols = st.columns(3)
            for i, suggestion in enumerate(suggestions):
                with cols[i % 3]:
                    if st.button(suggestion, key=f"suggestion_{i}", 
                               help="Click to ask this question",
                               use_container_width=True):
                        st.session_state.messages.append(("user", suggestion))
                        st.session_state.is_typing = True
                        st.rerun()
        
        # Display chat messages
        for role, message in st.session_state.messages:
            display_message(message, is_user=(role == "user"))
        
        # Display typing indicator
        if st.session_state.is_typing:
            display_typing_indicator()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input area
        st.markdown("---")
        
        # Text input
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Ask about any Indian stock, IPO, or market data...",
                key=f"user_input_{len(st.session_state.messages)}",
                placeholder="Type your question here...",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.button("🚀 Send", key="send_button", 
                                  use_container_width=True,
                                  disabled=st.session_state.is_typing)
        
        # Handle input
        if (send_button or user_input) and user_input.strip() and not st.session_state.is_typing:
            # Add user message
            st.session_state.messages.append(("user", user_input))
            st.session_state.is_typing = True
            st.rerun()
        
        # Process AI response
        if st.session_state.is_typing and st.session_state.messages:
            last_message = st.session_state.messages[-1]
            if last_message[0] == "user":
                # Get AI response
                response = get_ai_response(last_message[1])
                
                # Add AI response
                st.session_state.messages.append(("assistant", response))
                st.session_state.is_typing = False
                
                st.rerun()

if __name__ == "__main__":
    main()
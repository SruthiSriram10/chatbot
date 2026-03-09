"""
ENHANCED WEB CHATBOT - With better UI and features
"""
from flask import Flask, render_template, request, jsonify, session
from datetime import datetime as dt
import os
import sys
import uuid

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

app = Flask(__name__)
app.secret_key = 'enhanced-chatbot-2024'
app.config['SESSION_TYPE'] = 'filesystem'

# Try to import enhanced chatbot
try:
    from chatbot import chat_with_context, speak, test_api_connection
    CHATBOT_AVAILABLE = True
    print("✅ Enhanced chatbot loaded successfully")
except Exception as e:
    print(f"❌ Error loading chatbot: {e}")
    CHATBOT_AVAILABLE = False

# Store chats with context
chats = {}

@app.route('/')
def home():
    """Serve the main page"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    session_id = session['session_id']
    
    if session_id not in chats:
        chats[session_id] = []
        # Add welcome message
        chats[session_id].append({
            'type': 'bot',
            'content': 'Hello! I\'m your enhanced AI assistant. I can help you with programming, answer questions, tell jokes, and more! How can I assist you today? 😊',
            'timestamp': dt.now().strftime("%I:%M %p"),
            'avatar': '🤖'
        })
    
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
        
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get bot response with context
        if CHATBOT_AVAILABLE:
            bot_response = chat_with_context(user_message, session_id)
        else:
            bot_response = "I'm here to help! What would you like to know?"
        
        # Store in history
        if session_id not in chats:
            chats[session_id] = []
        
        # Add user message
        chats[session_id].append({
            'type': 'user',
            'content': user_message,
            'timestamp': dt.now().strftime("%I:%M %p"),
            'avatar': '👤'
        })
        
        # Add bot response
        chats[session_id].append({
            'type': 'bot',
            'content': bot_response,
            'timestamp': dt.now().strftime("%I:%M %p"),
            'avatar': '🤖'
        })
        
        # Keep only last 30 messages
        if len(chats[session_id]) > 30:
            chats[session_id] = chats[session_id][-30:]
        
        return jsonify({
            'response': bot_response,
            'timestamp': dt.now().strftime("%I:%M %p")
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'response': 'Sorry, I encountered an error. Please try again.',
            'timestamp': dt.now().strftime("%I:%M %p")
        })

@app.route('/history', methods=['GET'])
def get_history():
    """Get chat history"""
    session_id = session.get('session_id')
    if session_id and session_id in chats:
        return jsonify(chats[session_id])
    return jsonify([])

@app.route('/clear', methods=['POST'])
def clear_chat():
    """Clear chat history"""
    session_id = session.get('session_id')
    if session_id and session_id in chats:
        chats[session_id] = [{
            'type': 'bot',
            'content': 'Chat cleared! How can I help you now? 😊',
            'timestamp': dt.now().strftime("%I:%M %p"),
            'avatar': '🤖'
        }]
    return jsonify({'status': 'cleared'})

@app.route('/speak', methods=['POST'])
def text_to_speech():
    """Convert text to speech"""
    if not CHATBOT_AVAILABLE:
        return jsonify({'error': 'TTS not available'}), 400
    
    try:
        data = request.json
        text = data.get('text', '')
        
        if text:
            speak(text)
            return jsonify({'status': 'spoken'})
        else:
            return jsonify({'error': 'No text provided'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/suggest', methods=['GET'])
def get_suggestions():
    """Get suggested questions"""
    suggestions = [
        "What is Python?",
        "Tell me a joke",
        "What's the time?",
        "Explain AI",
        "Python vs Java",
        "Tell me a fact",
        "What is machine learning?",
        "How to learn programming?"
    ]
    return jsonify(suggestions)

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 ENHANCED CHATBOT WEB INTERFACE")
    print("=" * 70)
    print(f"📂 Directory: {current_dir}")
    print(f"🤖 Chatbot: {'✅ Available' if CHATBOT_AVAILABLE else '❌ Not available'}")
    print("\n✨ Features enabled:")
    print("  • Intelligent responses with context")
    print("  • Programming help with examples")
    print("  • Jokes and facts")
    print("  • Math calculations")
    print("  • AI/ML explanations")
    print("  • Comparisons and charts")
    print("\n🌐 Starting server...")
    print("👉 Open: http://localhost:5000")
    print("=" * 70)
    
    # Ensure templates directory exists
    templates_dir = os.path.join(current_dir, 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    app.run(debug=True, port=5000)
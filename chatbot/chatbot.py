"""
ENHANCED CHATBOT - With better AI responses
"""
from datetime import datetime
import pyttsx3
import random
import re
import json
from collections import defaultdict

print("🤖 Initializing Enhanced ChatBot...")

# -------------------
# Initialize TTS Engine
# -------------------
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)  # Slightly faster
    engine.setProperty('volume', 0.9)
    voices = engine.getProperty('voices')
    if voices:
        # Try to set a female voice if available
        for voice in voices:
            if 'female' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
    print("✅ TTS Engine initialized")
except Exception as e:
    print(f"⚠️ TTS Engine error: {e}")
    engine = None

def speak(text):
    """Speak the given text aloud"""
    if engine is None:
        return
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

# -------------------
# Enhanced Knowledge Base
# -------------------
class KnowledgeBase:
    def __init__(self):
        self.load_knowledge()
    
    def load_knowledge(self):
        # Programming Knowledge
        self.programming = {
            "python": {
                "description": "Python is a high-level, interpreted programming language known for its simplicity and readability. It supports multiple programming paradigms including procedural, object-oriented, and functional programming.",
                "features": [
                    "Easy to learn and read",
                    "Large standard library",
                    "Dynamic typing",
                    "Memory management automatic",
                    "Extensive third-party packages"
                ],
                "use_cases": [
                    "Web Development (Django, Flask)",
                    "Data Science (Pandas, NumPy)",
                    "Machine Learning (TensorFlow, PyTorch)",
                    "Automation and Scripting",
                    "Desktop Applications"
                ],
                "example": """```python
# Hello World in Python
print("Hello, World!")

# Simple function
def greet(name):
    return f"Hello, {name}!"

print(greet("User"))
```"""
            },
            "javascript": {
                "description": "JavaScript is a high-level, interpreted programming language that conforms to the ECMAScript specification. It is one of the core technologies of the World Wide Web.",
                "features": [
                    "Client-side scripting",
                    "Event-driven programming",
                    "Prototype-based object orientation",
                    "First-class functions",
                    "Dynamic typing"
                ],
                "use_cases": [
                    "Web Development",
                    "Mobile Apps (React Native)",
                    "Server-side (Node.js)",
                    "Game Development",
                    "Browser Extensions"
                ],
                "example": """```javascript
// Hello World in JavaScript
console.log("Hello, World!");

// Simple function
function greet(name) {
    return `Hello, ${name}!`;
}

console.log(greet("User"));
```"""
            },
            "java": {
                "description": "Java is a class-based, object-oriented programming language designed for portability across platforms. It follows the 'Write Once, Run Anywhere' principle.",
                "features": [
                    "Platform independence via JVM",
                    "Strong typing",
                    "Automatic memory management",
                    "Multi-threading support",
                    "Rich API"
                ]
            },
            "html": {
                "description": "HTML (HyperText Markup Language) is the standard markup language for creating web pages and web applications.",
                "features": [
                    "Defines structure of web pages",
                    "Uses tags to mark up content",
                    "Works with CSS and JavaScript",
                    "Semantic elements available",
                    "Cross-platform compatible"
                ],
                "example": """```html
<!DOCTYPE html>
<html>
<head>
    <title>My Page</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a paragraph.</p>
</body>
</html>
```"""
            },
            "css": {
                "description": "CSS (Cascading Style Sheets) is a stylesheet language used to describe the presentation of a document written in HTML.",
                "features": [
                    "Controls layout and design",
                    "Responsive design capabilities",
                    "Animations and transitions",
                    "Flexbox and Grid systems",
                    "Media queries for responsiveness"
                ]
            }
        }
        
        # General Knowledge
        self.general = {
            "science": {
                "physics": "Physics is the natural science that studies matter, its motion and behavior through space and time.",
                "chemistry": "Chemistry is the scientific discipline involved with elements and compounds composed of atoms, molecules, and ions.",
                "biology": "Biology is the natural science that studies life and living organisms."
            },
            "technology": {
                "ai": "Artificial Intelligence is the simulation of human intelligence in machines that are programmed to think and learn.",
                "ml": "Machine Learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed.",
                "blockchain": "Blockchain is a distributed ledger technology that maintains a secure and decentralized record of transactions."
            }
        }
        
        # Conversation Patterns
        self.patterns = {
            r"\b(hi|hello|hey|greetings)\b": {
                "responses": [
                    "Hello! How can I assist you today? 😊",
                    "Hi there! What can I help you with?",
                    "Hey! Nice to see you. How can I be of service?",
                    "Greetings! I'm here to help. What would you like to know?"
                ],
                "follow_up": "I can help with programming, general knowledge, or just chat!"
            },
            r"\bhow are you\b": {
                "responses": [
                    "I'm doing great, thank you for asking! How can I help you today?",
                    "I'm functioning perfectly! What can I assist you with?",
                    "All systems are operational! How can I be of service?"
                ]
            },
            r"\b(thank|thanks)\b": {
                "responses": [
                    "You're welcome! 😊",
                    "Happy to help!",
                    "My pleasure!",
                    "Anytime! Let me know if you need anything else."
                ]
            },
            r"\b(bye|goodbye|see you)\b": {
                "responses": [
                    "Goodbye! Have a wonderful day! 👋",
                    "See you later! Take care!",
                    "Bye! Feel free to come back if you have more questions!"
                ]
            },
            r"\b(who are you|what are you)\b": {
                "responses": [
                    "I'm an enhanced AI chatbot designed to help you with various questions about programming, technology, and general knowledge. How can I assist you today?",
                    "I'm your intelligent assistant powered by advanced AI algorithms. I can help with coding, answer questions, or just chat!"
                ]
            },
            r"\b(what can you do|help)\b": {
                "responses": [
                    "I can help you with:\n\n💻 **Programming**: Python, JavaScript, HTML, CSS, and more\n🔬 **Science & Technology**: AI, ML, Physics, Chemistry\n📚 **General Knowledge**: Answer questions on various topics\n⏰ **Time & Date**: Current time, date, day information\n💬 **Conversation**: Just chat and have fun!\n\nWhat would you like to know about?"
                ]
            }
        }
        
        # Math patterns
        self.math_patterns = {
            r"(\d+)\s*\+\s*(\d+)": lambda m: f"{m.group(1)} + {m.group(2)} = {int(m.group(1)) + int(m.group(2))}",
            r"(\d+)\s*-\s*(\d+)": lambda m: f"{m.group(1)} - {m.group(2)} = {int(m.group(1)) - int(m.group(2))}",
            r"(\d+)\s*\*\s*(\d+)": lambda m: f"{m.group(1)} × {m.group(2)} = {int(m.group(1)) * int(m.group(2))}",
            r"(\d+)\s*/\s*(\d+)": lambda m: f"{m.group(1)} ÷ {m.group(2)} = {int(m.group(1)) / int(m.group(2)):.2f}"
        }
        
        # Jokes
        self.jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why did the Python programmer not get married? Because he didn't like commitments!",
            "What's a programmer's favorite hangout place? The Foo Bar!",
            "Why do Java developers wear glasses? Because they can't C#!",
            "What's the object-oriented way to become wealthy? Inheritance!",
            "Why did the programmer quit his job? He didn't get arrays!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
            "Why do Python programmers prefer snakes? They hate spam!"
        ]
        
        # Facts
        self.facts = [
            "The first computer programmer was Ada Lovelace, who wrote algorithms for Charles Babbage's Analytical Engine in the 1840s.",
            "Python was named after Monty Python, not the snake!",
            "The first computer virus was created in 1983 and was called 'Elk Cloner'.",
            "The average person spends about 6.5 years of their life looking at screens.",
            "The first website is still online at info.cern.ch.",
            "There are over 700 different programming languages in existence.",
            "The term 'bug' in programming came from an actual moth found in a computer in 1947.",
            "JavaScript was created in just 10 days in 1995."
        ]

knowledge = KnowledgeBase()

# -------------------
# Enhanced Chatbot Function
# -------------------
def chat_with_bot(user_input):
    """Enhanced chatbot with better responses"""
    if not user_input or not user_input.strip():
        return "Please type a message."
    
    user_input = user_input.strip()
    user_lower = user_input.lower()
    now = datetime.now()
    
    # Handle time/date queries with more detail
    if "time" in user_lower and "date" in user_lower:
        return f"📅 **Current Date & Time:**\n{now.strftime('%A, %B %d, %Y')}\n⏰ **Time:** {now.strftime('%I:%M:%S %p')}\n🌍 **Timezone:** Local"
    elif "time" in user_lower:
        return f"⏰ **Current Time:** {now.strftime('%I:%M:%S %p')}\n🕐 **24-hour format:** {now.strftime('%H:%M:%S')}"
    elif "date" in user_lower:
        return f"📆 **Today's Date:** {now.strftime('%B %d, %Y')}\n📅 **Day:** {now.strftime('%A')}"
    elif "day" in user_lower:
        return f"📅 **Today is {now.strftime('%A')}**\n🗓️ **Full date:** {now.strftime('%B %d, %Y')}"
    
    # Handle math calculations
    for pattern, calculator in knowledge.math_patterns.items():
        match = re.search(pattern, user_input)
        if match:
            return f"🧮 **Calculation Result:**\n{calculator(match)}"
    
    # Handle jokes
    if "joke" in user_lower or "funny" in user_lower:
        return f"😂 **Here's a joke for you:**\n\n{random.choice(knowledge.jokes)}"
    
    # Handle facts
    if "fact" in user_lower or "interesting" in user_lower:
        return f"📚 **Did you know?**\n\n{random.choice(knowledge.facts)}"
    
    # Handle programming questions
    for lang, info in knowledge.programming.items():
        if lang in user_lower:
            response = f"**About {lang.capitalize()}:**\n\n"
            response += f"📖 **Description:** {info['description']}\n\n"
            
            if 'features' in info:
                response += "✨ **Key Features:**\n"
                for feature in info['features'][:4]:  # Show top 4 features
                    response += f"• {feature}\n"
                response += "\n"
            
            if 'use_cases' in info:
                response += "🚀 **Common Use Cases:**\n"
                for use in info['use_cases'][:4]:
                    response += f"• {use}\n"
                response += "\n"
            
            if 'example' in info:
                response += f"💻 **Example:**\n{info['example']}\n"
            
            response += "\nWould you like to know more about any specific aspect?"
            return response
    
    # Handle AI/ML questions
    if "ai" in user_lower or "artificial intelligence" in user_lower:
        return """**About Artificial Intelligence (AI):**

🤖 **Definition:** AI is the simulation of human intelligence in machines.

📊 **Main Branches:**
• Machine Learning
• Deep Learning
• Natural Language Processing
• Computer Vision
• Robotics

💡 **Applications:**
• Virtual Assistants (Siri, Alexa)
• Recommendation Systems
• Autonomous Vehicles
• Healthcare Diagnostics
• Financial Predictions

Would you like to know more about any specific aspect of AI?"""
    
    if "machine learning" in user_lower or "ml" in user_lower:
        return """**About Machine Learning (ML):**

🎯 **Definition:** ML is a subset of AI that enables systems to learn from data.

📚 **Types of Machine Learning:**
1. **Supervised Learning** - Learning with labeled data
2. **Unsupervised Learning** - Finding patterns in unlabeled data
3. **Reinforcement Learning** - Learning through rewards

🔧 **Popular Algorithms:**
• Linear/Logistic Regression
• Decision Trees
• Neural Networks
• Support Vector Machines
• K-Means Clustering

🌐 **Common Frameworks:**
• TensorFlow
• PyTorch
• Scikit-learn
• Keras

Want to dive deeper into any of these topics?"""
    
    # Check conversation patterns
    for pattern, data in knowledge.patterns.items():
        if re.search(pattern, user_lower):
            response = random.choice(data['responses'])
            if 'follow_up' in data:
                response += f"\n\n💡 {data['follow_up']}"
            return response
    
    # Handle question words
    if user_input.endswith('?'):
        if user_lower.startswith(('what', 'who', 'where', 'when', 'why', 'how')):
            topic = ' '.join(user_lower.split()[1:]).replace('?', '')
            return f"🤔 **Great question about '{topic}'!**\n\nI'd be happy to help you learn about this. To give you the most accurate information, could you please be more specific about what aspect of '{topic}' interests you?"
    
    # Handle specific topics
    if "python" in user_lower and "vs" in user_lower:
        if "java" in user_lower:
            return """**Python vs Java Comparison:**

🐍 **Python:**
• Dynamically typed
• Easy to learn
• Great for data science
• Faster development

☕ **Java:**
• Statically typed
• More verbose
• Better for large enterprise apps
• Faster execution

**Which one to choose?**
- Choose Python for: Data science, AI, quick prototyping
- Choose Java for: Large-scale enterprise apps, Android development"""
    
    # Default intelligent response
    default_responses = [
        f"📝 **Regarding '{user_input}':**\n\nThat's an interesting topic! To provide you with the most relevant information, could you tell me more about what specifically you'd like to know?",
        
        f"🤔 **About your question:**\n\nI understand you're asking about '{user_input}'. Let me help you with that. Could you provide a bit more context or specify what aspect interests you most?",
        
        f"💡 **Here's what I know:**\n\nBased on your question about '{user_input}', I can tell you that this is a fascinating topic! Would you like me to explain the basics, or is there something specific you're curious about?",
        
        f"🎯 **Let me help you with '{user_input}':**\n\nThis is a great question! To give you the best answer, could you clarify whether you're interested in:\n• Basic concepts\n• Practical applications\n• Advanced topics\n• Examples and use cases"
    ]
    
    return random.choice(default_responses)

# -------------------
# Context-aware responses (remembers previous questions)
# -------------------
class ContextAwareBot:
    def __init__(self):
        self.context = defaultdict(list)
        self.conversation_history = []
    
    def get_response_with_context(self, user_input, session_id="default"):
        """Get response considering conversation context"""
        
        # Store in history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Get base response
        response = chat_with_bot(user_input)
        
        # Store response
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Add context if available
        if len(self.conversation_history) > 2:
            last_topic = self._extract_topic(self.conversation_history[-3]["content"])
            if last_topic:
                response += f"\n\n💭 By the way, we were discussing {last_topic} earlier. Would you like to continue that conversation?"
        
        return response
    
    def _extract_topic(self, text):
        """Extract main topic from text"""
        words = text.lower().split()
        topics = ['python', 'javascript', 'java', 'html', 'css', 'ai', 'ml', 'programming']
        for word in words:
            if word in topics:
                return word
        return None

# Create context-aware bot instance
context_bot = ContextAwareBot()

# -------------------
# Compatibility functions
# -------------------
def test_api_connection():
    """Mock function for compatibility"""
    print("✅ Enhanced chatbot - No external API needed")
    return True

def initialize_client():
    """Mock function for compatibility"""
    return True

def chat_with_context(user_input, session_id="default"):
    """Get response with context awareness"""
    return context_bot.get_response_with_context(user_input, session_id)

# -------------------
# Terminal testing with context
# -------------------
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🤖 ENHANCED CHATBOT - Terminal Mode")
    print("=" * 70)
    print("✨ Features:")
    print("• Intelligent responses with context")
    print("• Programming help with examples")
    print("• Math calculations")
    print("• Jokes and facts")
    print("• AI/ML explanations")
    print("• Comparison charts")
    print("• Time/Date information")
    print("=" * 70)
    print("Type 'exit' to quit, 'clear' to reset context\n")
    
    session_id = "terminal_session"
    
    while True:
        try:
            user_msg = input("\nYou: ").strip()
            if not user_msg:
                continue
                
            if user_msg.lower() == 'exit':
                print("\n👋 Thank you for chatting! Goodbye!")
                if engine:
                    speak("Thank you for chatting! Goodbye!")
                break
                
            if user_msg.lower() == 'clear':
                context_bot.conversation_history = []
                print("🔄 Context cleared!")
                continue
            
            if user_msg.lower() == 'help':
                print("\n📚 **Available Commands:**")
                print("• Ask any question naturally")
                print("• 'time' - Get current time")
                print("• 'date' - Get today's date")
                print("• 'joke' - Hear a joke")
                print("• 'fact' - Learn a fact")
                print("• 'clear' - Reset conversation")
                print("• 'exit' - Quit")
                continue
            
            # Get response with context
            reply = chat_with_context(user_msg, session_id)
            
            print(f"\nBot: {reply}")
            
            # Optional: Speak response
            if engine and len(reply) < 200:
                speak_response = input("\n🔊 Speak response? (y/n): ").lower()
                if speak_response == 'y':
                    speak(reply)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
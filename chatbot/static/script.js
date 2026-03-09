document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    const typingIndicator = document.getElementById('typingIndicator');
    const stopSpeechButton = document.getElementById('stopSpeech');
    const ttsToggle = document.getElementById('ttsToggle');
    const currentTimeElement = document.getElementById('currentTime');
    
    // State
    let ttsEnabled = true;
    
    // Initialize
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
    loadChatHistory();
    
    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    if (stopSpeechButton) {
        stopSpeechButton.addEventListener('click', stopSpeech);
    }
    
    if (ttsToggle) {
        ttsToggle.addEventListener('change', function() {
            ttsEnabled = this.checked;
            showNotification(`Voice ${ttsEnabled ? 'enabled' : 'disabled'}`);
        });
    }
    
    // Functions
    function updateCurrentTime() {
        const now = new Date();
        currentTimeElement.textContent = now.toLocaleTimeString();
    }
    
    async function sendMessage() {
        const message = userInput.value.trim();
        
        if (!message) return;
        
        // Add user message
        addMessage(message, 'user');
        
        // Clear and reset input
        userInput.value = '';
        userInput.style.height = 'auto';
        
        // Show typing indicator
        showTypingIndicator();
        
        try {
            // Send to server
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: message,
                    tts: ttsEnabled 
                })
            });
            
            const data = await response.json();
            
            // Hide typing indicator
            hideTypingIndicator();
            
            if (response.ok) {
                // Add bot response
                addMessage(data.response, 'bot', data.timestamp);
            } else {
                addMessage(`Error: ${data.error}`, 'bot');
            }
            
        } catch (error) {
            hideTypingIndicator();
            addMessage('Network error. Please try again.', 'bot');
            console.error('Error:', error);
        }
        
        scrollToBottom();
    }
    
    function addMessage(text, sender, timestamp = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const now = new Date();
        const time = timestamp || `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
        
        const avatarIcon = sender === 'user' ? 'fas fa-user' : 'fas fa-robot';
        
        // Format text with line breaks and emoji support
        const formattedText = text.replace(/\n/g, '<br>');
        
        messageDiv.innerHTML = `
            <div class="avatar">
                <i class="${avatarIcon}"></i>
            </div>
            <div class="message-content">
                <p class="text">${formattedText}</p>
                <span class="timestamp">${time}</span>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function showTypingIndicator() {
        typingIndicator.style.display = 'flex';
        scrollToBottom();
    }
    
    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
    }
    
    function scrollToBottom() {
        setTimeout(() => {
            chatMessages.parentElement.scrollTop = chatMessages.parentElement.scrollHeight;
        }, 100);
    }
    
    async function loadChatHistory() {
        try {
            const response = await fetch('/history');
            const history = await response.json();
            
            // Clear existing messages except welcome
            const existingMessages = chatMessages.querySelectorAll('.message');
            for (let i = 1; i < existingMessages.length; i++) {
                existingMessages[i].remove();
            }
            
            // Load history
            history.forEach(entry => {
                addMessage(entry.user, 'user', entry.timestamp);
                addMessage(entry.bot, 'bot', entry.timestamp);
            });
            
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }
    
    async function clearChat() {
        if (confirm('Clear all chat history?')) {
            try {
                await fetch('/clear', { method: 'POST' });
                
                // Clear UI except welcome message
                const existingMessages = chatMessages.querySelectorAll('.message');
                for (let i = 1; i < existingMessages.length; i++) {
                    existingMessages[i].remove();
                }
                
                addMessage('Chat history cleared.', 'bot');
                
            } catch (error) {
                console.error('Error clearing chat:', error);
            }
        }
    }
    
    async function stopSpeech() {
        try {
            await fetch('/tts', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ action: 'stop' })
            });
            showNotification('Speech stopped');
        } catch (error) {
            console.error('Error stopping speech:', error);
        }
    }
    
    function showNotification(message) {
        // Create notification
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #667eea;
            color: white;
            padding: 12px 24px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    // Quick actions (accessible from HTML buttons)
    window.quickAction = async function(action) {
        const questions = {
            'time': 'What time is it?',
            'date': 'What is the date today?',
            'day': 'What day is today?'
        };
        
        if (questions[action]) {
            userInput.value = questions[action];
            sendMessage();
        }
    };
    
    window.clearChat = clearChat;
    
    // Add CSS for notifications
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
});
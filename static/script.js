// State Management
let chatHistory = [];
let currentChat = [];
let isDarkMode = localStorage.getItem('darkMode') === 'true';
let animationsEnabled = localStorage.getItem('animationsEnabled') !== 'false';
let audioEnabled = localStorage.getItem('audioEnabled') !== 'false';
let currentLanguage = localStorage.getItem('currentLanguage') || 'English';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
    }

    // Initialize voice button state
    updateVoiceButtonState();

    // Set initial language
    document.getElementById('languageSelect').value = currentLanguage;
    applyLanguage(currentLanguage);

    const questionInput = document.getElementById('questionInput');

    // Character limit and auto-resize
    questionInput.addEventListener('input', function() {
        if (this.value.length > 500) {
            this.value = this.value.substring(0, 500);
        }

        // Auto-resize textarea
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });

    // Send message on Ctrl+Enter or Enter (mobile)
    questionInput.addEventListener('keypress', function(e) {
        if ((e.key === 'Enter' && e.ctrlKey) || (e.key === 'Enter' && window.innerWidth <= 768)) {
            e.preventDefault();
            askQuestion();
        }
    });

    // Load chat history from localStorage
    loadChatHistory();
});

// Language switching function
function changeLanguage(lang) {
    currentLanguage = lang;
    localStorage.setItem('currentLanguage', lang);
    applyLanguage(lang);
    
    // If welcome section is displayed, refresh it with new language
    if (currentChat.length === 0) {
        startNewChat();
    }
}

// Apply language to all elements
function applyLanguage(lang) {
    const isHindi = lang === 'Hindi';
    
    // Change document language (no direction change to keep layout same)
    document.documentElement.lang = isHindi ? 'hi' : 'en';
    document.body.classList.toggle('hindi-mode', isHindi);
    
    // Update all elements with data attributes
    document.querySelectorAll('[data-en][data-hi]').forEach(element => {
        const text = isHindi ? element.getAttribute('data-hi') : element.getAttribute('data-en');
        const isBtnText = element.classList.contains('btn-text');
        
        if (isBtnText) {
            element.textContent = text;
        } else if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            element.placeholder = text;
        } else if (element.children.length === 0 || element.classList.contains('logo-name')) {
            element.textContent = text;
        }
    });

    // Update placeholder for textarea
    document.getElementById('questionInput').placeholder = isHindi 
        ? 'खेती, फसल, मौसम, उर्वरक के बारे में पूछें...' 
        : 'Ask me about farming, crops, weather, fertilizers...';
}

// Load chat history
function loadChatHistory() {
    const saved = localStorage.getItem('chatHistory');
    if (saved) {
        try {
            chatHistory = JSON.parse(saved).slice(-50); // Keep last 50 chats
            updateHistoryUI();
        } catch (e) {
            console.error('Error loading chat history:', e);
        }
    }
}

// Update history UI with delete buttons
function updateHistoryUI() {
    const historyList = document.getElementById('chatHistory');
    historyList.innerHTML = '';

    chatHistory.forEach((chat, index) => {
        const itemContainer = document.createElement('div');
        itemContainer.className = 'history-item-container';
        
        const item = document.createElement('div');
        item.className = 'history-item';
        item.textContent = chat.title || `Chat ${index + 1}`;
        item.onclick = () => loadChat(index);
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'history-delete-btn';
        deleteBtn.innerHTML = '<i class="fas fa-trash"></i>';
        deleteBtn.title = 'Delete this chat';
        deleteBtn.onclick = (e) => {
            e.stopPropagation();
            deleteChat(index);
        };
        
        itemContainer.appendChild(item);
        itemContainer.appendChild(deleteBtn);
        historyList.appendChild(itemContainer);
    });
}

// Start new chat
function startNewChat() {
    // Save current chat if it has messages
    if (currentChat.length > 0) {
        saveChatToHistory();
    }
    
    currentChat = [];
    
    // Determine language for welcome section
    const isHindi = currentLanguage === 'Hindi';
    const title = isHindi ? 'कृषि सहाय' : 'KrishiSahay';
    const subtitle = isHindi ? 'आपका AI कृषि साथी' : 'Your AI Farming Companion';
    const smartCrops = isHindi ? 'स्मार्ट फसलें' : 'Smart Crops';
    const smartCropsDesc = isHindi ? 'AI-संचालित फसल सुझाव' : 'AI-powered crop recommendations';
    const fertilizers = isHindi ? 'उर्वरक' : 'Fertilizers';
    const fertilizersDesc = isHindi ? 'पोषण मार्गदर्शन और योजना' : 'Nutrient guidance & planning';
    const rotation = isHindi ? 'रोटेशन' : 'Rotation';
    const rotationDesc = isHindi ? 'फसल चक्र अनुकूलन' : 'Crop rotation optimization';
    const weather = isHindi ? 'मौसम' : 'Weather';
    const weatherDesc = isHindi ? 'रीयल-टाइम मौसम अंतर्दृष्टि' : 'Real-time weather insights';
    
    document.getElementById('messagesWrapper').innerHTML = `
        <div class="welcome-section-gradient">
            <div class="welcome-hero">
                <div class="hero-icon">🌾</div>
                <h1 class="hero-title">${title}</h1>
                <p class="hero-subtitle">${subtitle}</p>
            </div>
            
            <div class="feature-cards">
                <div class="feature-card" style="background: linear-gradient(135deg, #2d5016 0%, #1a3a0a 100%);">
                    <div class="card-icon">🌱</div>
                    <h3>${smartCrops}</h3>
                    <p>${smartCropsDesc}</p>
                </div>
                <div class="feature-card" style="background: linear-gradient(135deg, #8b6f47 0%, #5a4a3a 100%);">
                    <div class="card-icon">🧪</div>
                    <h3>${fertilizers}</h3>
                    <p>${fertilizersDesc}</p>
                </div>
                <div class="feature-card" style="background: linear-gradient(135deg, #3d6930 0%, #2a4620 100%);">
                    <div class="card-icon">🔄</div>
                    <h3>${rotation}</h3>
                    <p>${rotationDesc}</p>
                </div>
                <div class="feature-card" style="background: linear-gradient(135deg, #d4a574 0%, #a0894a 100%);">
                    <div class="card-icon">⛅</div>
                    <h3>${weather}</h3>
                    <p>${weatherDesc}</p>
                </div>
            </div>
        </div>
    `;
    document.getElementById('questionInput').value = '';
}

// Load a specific chat
function loadChat(index) {
    if (chatHistory[index]) {
        currentChat = chatHistory[index].messages;
        displayMessages();
    }
}

// Main ask question function
async function askQuestion() {
    const question = document.getElementById('questionInput').value.trim();
    const language = document.getElementById('languageSelect').value;

    if (!question) {
        showAlert('Please enter a question!');
        return;
    }

    if (!animationsEnabled) {
        document.documentElement.style.setProperty('--transition', 'none');
    }

    // Remove welcome section if it exists
    const welcome = document.querySelector('.welcome-section-gradient');
    if (welcome) {
        welcome.remove();
    }

    // Add user message to chat
    currentChat.push({
        type: 'user',
        content: question,
        timestamp: new Date()
    });

    displayMessages();
    scrollToBottom();

    // Clear input
    document.getElementById('questionInput').value = '';
    document.getElementById('questionInput').style.height = 'auto';

    // Show loading indicator with ChatGPT-style typing
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant';
    loadingDiv.innerHTML = `
        <div class="unique-loading-container">
            <div class="farming-loader">
                <div class="crop-sprite">🌾</div>
                <div class="pulses">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            <div class="loading-text">
                <span class="dot">.</span>
                <span class="dot">.</span>
                <span class="dot">.</span>
            </div>
        </div>
    `;
    document.getElementById('messagesWrapper').appendChild(loadingDiv);
    scrollToBottom();

    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                language: language,
                chat_history: currentChat.map(msg => ({
                    type: msg.type,
                    content: msg.content
                }))
            })
        });

        const data = await response.json();

        // Remove loading indicator
        loadingDiv.remove();

        if (response.ok) {
            // Add assistant message
            currentChat.push({
                type: 'assistant',
                content: data.answer,
                timestamp: new Date()
            });

            displayMessages();

            // Handle audio if enabled
            if (data.audio_url) {
                const audioSection = document.getElementById('audioSection');
                const audioPlayer = document.getElementById('audioPlayer');
                audioPlayer.src = data.audio_url;
                audioSection.style.display = 'block';
                
                // Store current audio URL for download
                window.currentAudioUrl = data.audio_url;
                
                // Auto-play if enabled
                if (audioEnabled) {
                    audioPlayer.play().catch(err => console.log('Audio play failed:', err));
                }
            }

            // Save to chat history (updates existing or creates new)
            saveChatToHistory();

            scrollToBottom();
        } else {
            showError('Error: ' + (data.error || 'Unknown error occurred'));
            currentChat.pop(); // Remove failed message
        }
    } catch (error) {
        console.error('Error:', error);
        loadingDiv.remove();
        showError('Request failed: ' + error.message);
        currentChat.pop(); // Remove failed message
    }

    if (!animationsEnabled) {
        document.documentElement.style.setProperty('--transition', 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)');
    }
}

// Display messages
function displayMessages() {
    const wrapper = document.getElementById('messagesWrapper');
    
    // Clear existing messages (but keep welcome if no current chat)
    if (currentChat.length > 0) {
        wrapper.innerHTML = '';
    }

    currentChat.forEach((msg, index) => {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${msg.type}`;

        if (msg.type === 'assistant') {
            msgDiv.innerHTML = `
                <div class="message-bubble">
                    ${escapeHtml(msg.content)}
                </div>
            `;
        } else {
            msgDiv.innerHTML = `
                <div class="message-bubble">
                    ${escapeHtml(msg.content)}
                </div>
            `;
        }

        wrapper.appendChild(msgDiv);

        // Add staggered animation
        if (animationsEnabled) {
            msgDiv.style.animation = `slideIn 0.3s ease-out ${index * 0.05}s both`;
        }
    });
}

// Save chat to history - saves complete current chat
function saveChatToHistory() {
    if (currentChat.length === 0) return;
    
    // Get title from first user message
    const firstUserMsg = currentChat.find(msg => msg.type === 'user');
    if (!firstUserMsg) return;
    
    const title = firstUserMsg.content.substring(0, 30) + (firstUserMsg.content.length > 30 ? '...' : '');
    
    // Check if this chat already exists in history
    const existingIndex = chatHistory.findIndex(chat => 
        chat.messages && chat.messages[0] && chat.messages[0].content === firstUserMsg.content
    );
    
    if (existingIndex !== -1) {
        // Update existing chat
        chatHistory[existingIndex] = {
            title: title,
            messages: JSON.parse(JSON.stringify(currentChat)), // Deep copy
            timestamp: new Date()
        };
    } else {
        // Create new chat entry
        chatHistory.push({
            title: title,
            messages: JSON.parse(JSON.stringify(currentChat)), // Deep copy
            timestamp: new Date()
        });
    }
    
    // Keep only last 50 chats
    if (chatHistory.length > 50) {
        chatHistory.shift();
    }
    
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    updateHistoryUI();
}

// Delete specific chat from history
function deleteChat(index) {
    if (confirm('Delete this chat?')) {
        chatHistory.splice(index, 1);
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
        updateHistoryUI();
        
        // If the deleted chat was the current one, start new chat
        if (currentChat.length === 0 || index === chatHistory.length) {
            startNewChat();
        }
    }
}

// Utility functions
function scrollToBottom() {
    const container = document.querySelector('.messages-container');
    setTimeout(() => {
        container.scrollTop = container.scrollHeight;
    }, 100);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function showAlert(message) {
    alert(message);
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #ef4444;
        color: white;
        padding: 16px 20px;
        border-radius: 8px;
        z-index: 999;
        animation: slideIn 0.3s ease-out;
    `;
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);

    setTimeout(() => {
        errorDiv.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => errorDiv.remove(), 300);
    }, 3000);
}

// Theme toggle
function toggleTheme() {
    isDarkMode = !isDarkMode;
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', isDarkMode);
}

// Settings modal
function toggleSettings() {
    const modal = document.getElementById('settingsModal');
    modal.style.display = modal.style.display === 'none' ? 'flex' : 'none';

    // Update checkboxes
    if (modal.style.display === 'flex') {
        document.getElementById('audioToggle').checked = audioEnabled;
        document.getElementById('animationToggle').checked = animationsEnabled;

        document.getElementById('audioToggle').onchange = function() {
            audioEnabled = this.checked;
            localStorage.setItem('audioEnabled', audioEnabled);
            updateVoiceButtonState();
        };

        document.getElementById('animationToggle').onchange = function() {
            animationsEnabled = this.checked;
            localStorage.setItem('animationsEnabled', animationsEnabled);
        };
    }
}

// Toggle audio from header button
function toggleAudioFromHeader() {
    audioEnabled = !audioEnabled;
    localStorage.setItem('audioEnabled', audioEnabled);
    updateVoiceButtonState();
}

// Update voice button visual state
function updateVoiceButtonState() {
    const btn = document.getElementById('voiceToggleBtn');
    if (audioEnabled) {
        btn.classList.remove('audio-disabled');
    } else {
        btn.classList.add('audio-disabled');
    }
}

// Close modal on outside click
document.addEventListener('click', function(e) {
    const modal = document.getElementById('settingsModal');
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

// Help function
function showHelp() {
    alert(`KrishiSahay - Your AI Farming Assistant

🌾 Features:
• Ask about crop cultivation
• Get fertilizer recommendations
• Learn about crop rotation
• Get weather information
• Support for English & Hindi

💡 Tips:
• Be specific about your crops
• Include location for local advice
• Use Ctrl+Enter to send quickly
• Enable audio for voice responses

📱 Available on mobile too!`);
}

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);

// Download audio function
function downloadAudio() {
    if (!window.currentAudioUrl) {
        alert('No audio available to download');
        return;
    }

    const audioUrl = window.currentAudioUrl;
    const timestamp = new Date().toLocaleTimeString().replace(/:/g, '-');
    const filename = `KrishiSahay_response_${timestamp}.mp3`;

    // Create a temporary link and trigger download
    const link = document.createElement('a');
    link.href = audioUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Toggle audio from header button with proper event handling
function toggleAudioFromHeader() {
    audioEnabled = !audioEnabled;
    localStorage.setItem('audioEnabled', audioEnabled);
    updateVoiceButtonState();
    
    // Provide visual feedback
    const btn = document.getElementById('voiceToggleBtn');
    if (btn) {
        btn.style.transform = 'scale(0.95)';
        setTimeout(() => {
            btn.style.transform = 'scale(1)';
        }, 100);
    }
}

// Update voice button visual state
function updateVoiceButtonState() {
    const btn = document.getElementById('voiceToggleBtn');
    if (!btn) return;
    
    if (audioEnabled) {
        btn.classList.remove('audio-disabled');
        btn.title = 'Voice Output: ON';
    } else {
        btn.classList.add('audio-disabled');
        btn.title = 'Voice Output: OFF';
    }
}


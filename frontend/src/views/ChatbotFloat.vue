<template>
    <div>
        <!-- 悬浮按钮 -->
        <div class="chatbot-float-button" @click="toggleChat">
            <i class="fas fa-comment-dots"></i>
        </div>

        <!-- 聊天对话框 -->
        <div v-if="showChat" class="chatbot-dialog">
            <div class="chatbot-header">
                <span>DeepSeek 助手</span>
                <button @click="toggleChat" class="chatbot-close-btn">
                    <i class="fas fa-times"></i>
                </button>
            </div>

            <div class="chatbot-messages">
                <div v-for="(msg, index) in messages" :key="index" :class="['chatbot-message', msg.sender]">
                    <div class="chatbot-message-content">{{ msg.text }}</div>
                </div>
            </div>

            <div class="chatbot-input-area">
                <input v-model="userInput" @keyup.enter="sendMessage" placeholder="输入您的问题..." class="chatbot-input" />
                <button @click="sendMessage" class="chatbot-send-btn">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ChatbotFloat',
    data() {
        return {
            showChat: false,
            userInput: '',
            messages: [
                { text: '您好！我是DeepSeek助手，有什么可以帮您的吗？', sender: 'bot' }
            ]
        }
    },
    methods: {
        toggleChat() {
            this.showChat = !this.showChat
        },
        sendMessage() {
            if (!this.userInput.trim()) return

            // 添加用户消息
            this.messages.push({
                text: this.userInput,
                sender: 'user'
            })

            const userMessage = this.userInput
            this.userInput = ''

            // 模拟API调用
            this.getBotResponse(userMessage)
        },
        async getBotResponse(userMessage) {
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer sk-b980ba2bac8142cdadbe10a0155f4ec4'
                    },
                    body: JSON.stringify({
                        messages: [
                            { role: 'user', content: userMessage }
                        ]
                    })
                });

                const data = await response.json();
                this.messages.push({
                    text: data.reply,
                    sender: 'bot'
                });

            } catch (error) {
                this.messages.push({
                    text: '抱歉，请求API时出错: ' + error.message,
                    sender: 'bot'
                });
            }
        }

    }
}
</script>

<style scoped>
/* 悬浮按钮样式 */
.chatbot-float-button {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 60px;
    height: 60px;
    background-color: #4f46e5;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 9999;
    font-size: 24px;
    transition: all 0.3s ease;
}

.chatbot-float-button:hover {
    background-color: #4338ca;
    transform: scale(1.05);
}

/* 对话框样式 */
.chatbot-dialog {
    position: fixed;
    bottom: 100px;
    right: 30px;
    width: 350px;
    max-height: 500px;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    z-index: 9998;
    overflow: hidden;
}

.chatbot-header {
    padding: 15px;
    background-color: #4f46e5;
    color: white;
    font-weight: bold;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chatbot-close-btn {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    font-size: 16px;
}

.chatbot-messages {
    flex: 1;
    padding: 15px;
    overflow-y: auto;
    max-height: 400px;
}

.chatbot-message {
    margin-bottom: 12px;
    display: flex;
}

.chatbot-message.user {
    justify-content: flex-end;
}

.chatbot-message.bot {
    justify-content: flex-start;
}

.chatbot-message-content {
    max-width: 80%;
    padding: 10px 15px;
    border-radius: 18px;
}

.chatbot-message.user .chatbot-message-content {
    background-color: #4f46e5;
    color: white;
    border-bottom-right-radius: 4px;
}

.chatbot-message.bot .chatbot-message-content {
    background-color: #f3f4f6;
    color: #111827;
    border-bottom-left-radius: 4px;
}

.chatbot-input-area {
    display: flex;
    padding: 12px;
    border-top: 1px solid #e5e7eb;
}

.chatbot-input {
    flex: 1;
    padding: 10px 15px;
    border: 1px solid #d1d5db;
    border-radius: 20px;
    outline: none;
    margin-right: 10px;
}

.chatbot-input:focus {
    border-color: #4f46e5;
}

.chatbot-send-btn {
    width: 40px;
    height: 40px;
    background-color: #4f46e5;
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.chatbot-send-btn:hover {
    background-color: #4338ca;
}
</style>
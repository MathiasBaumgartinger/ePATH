<template>
    <div class="chatbox-container">
        <div class="container">
            <h1>Your personal counsellor</h1>
            <div class="messageBox mt-8">
                <template v-for="(message, index) in messages" :key="index">
                    <div v-if="message.role != 'system'" :class="message.role == 'user' ? 'messageFromUser' : 'messageFromAssitant'">
                        <div :class="message.role == 'user' ? 'userMessageWrapper' : 'assitantMessageWrapper'">
                            <!-- render markdown content -->
                            <Markdown
                              :content="message.content"
                              :plugins="[remarkGfm]"
                              :class="message.role == 'user' ? 'userMessageContent' : 'assitantMessageContent'"
                            />
                        </div>
                    </div>
                </template>
            </div>
            <div class="inputContainer">
                <input v-model="currentMessage" @keyup.enter="sendMessage(currentMessage)" type="text" class="messageInput"
                    placeholder="Ask me anything..." />
                <button @click="sendMessage(currentMessage)" class="askButton">
                    Ask
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { Markdown } from 'vue-markdown-next';
import remarkGfm from 'remark-gfm';
import { useChatHistoryStore } from './store.js'

export default {
  name: 'ChatBox',
  components: { Markdown },
    data() {
        return {
            currentMessage: '',
        };
    },
    computed: {
        store() {
            return useChatHistoryStore();
        },
        messages() {
            return this.store.messages;
        }
    },
    methods: {
        async sendMessage(message) {
            if (!message) return;
            this.store.messages.push({ role: 'user', content: message });
            this.currentMessage = '';
            await axios
                .post('/chat/api/', {
                    type: 'message',
                    content: message,
                    // TODO: do not hardcode this
                    user_uuid: '12345',
                })
                .then((response) => {
                    console.log(response); 
                });

            await axios
                .post('/chat/llm_api/', {
                    messages: this.store.messages,
                })
                .then((response) => {
                    console.log(response);

                    this.store.messages.push({
                        role: 'assistant',
                        content: response.data.response, // Access the 'data' property of the response object
                    });
                });

        },
    },
};
</script>

<style scoped>
/* container centering */
.chatbox-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.container {
  width: 90vw;
  max-width: 600px;
  height: 80vh;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: 'Roboto', sans-serif;
}

.messageBox {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 16px;
}

/* message alignment */
.messageFromUser {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 8px;
}
.messageFromAssitant {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 8px;
}

/* message bubbles */
.userMessageWrapper {
  background-color: #dcf8c6;
  border-radius: 16px 16px 0 16px;
  padding: 8px 12px;
  max-width: 70%;
}
.assitantMessageWrapper {
  background-color: #f1f0f0;
  border-radius: 16px 16px 16px 0;
  padding: 8px 12px;
  max-width: 70%;
}

/* input area */
.inputContainer {
  padding: 12px;
  border-top: 1px solid #ddd;
  display: flex;
}
.messageInput {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 16px;
  outline: none;
}
.askButton {
  margin-left: 8px;
  padding: 8px 16px;
  border: none;
  background-color: #4caf50;
  color: white;
  border-radius: 16px;
  cursor: pointer;
}
.askButton:hover {
  background-color: #45a049;
}

/* header styling */
.container h1 {
  text-align: center;
  margin: 16px 0;
  font-size: 1.5em;
}
</style>
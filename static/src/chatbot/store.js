import { defineStore } from "pinia";
import axios from "axios";

export const useChatHistoryStore = defineStore("chatbot", {
  state: () => ({
    messages: []
  }),
  getters: {
    isStoreEmpty() {
        return this.messages.length === 0;
    },
    containsSystemPrompt() {
        return this.messages.some(msg => msg.role === 'system');
    }
  },
  actions: {
    fetchMessages() {},
    async getSystemPrompt() {
        // TODO: do not hardcode this
        let user_uuid = 1;
        // Fetch the system prompt for the chatbot
        const { data } = await axios.get(`/questionnaire/system-prompt/${user_uuid}`, {
            params: { user_uuid },
        });
        this.messages.push(data);
    }
  },
  persist: {
    storage: sessionStorage, // data in sessionStorage is cleared when the page session ends.
  },
});

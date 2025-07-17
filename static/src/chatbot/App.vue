<script setup>
import Chat from './Chat.vue'
import { useChatHistoryStore } from './store.js'
import { onMounted } from 'vue'

// Initialize Pinia store for chat history
const store = useChatHistoryStore()

onMounted(() => {
    if (!store.containsSystemPrompt) {
        store.getSystemPrompt();
    } 
})
</script>

<template>
  <main>
    <div class="chat-container">
      <Chat />
    </div> 
  </main>
</template>

<style scoped>
</style>

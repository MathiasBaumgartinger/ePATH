<template>
  <div class="summary-container p-8">
    <h1 class="text-2xl font-bold mb-4">Thank you for your submission!</h1>
    <p class="mb-6">Your questionnaire has been submitted successfully. You can now discuss your findings with our AI assistant.</p>
    <button @click="goToChat" class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
      Discuss Your Findings
    </button>
  </div>
</template>

<script setup>
function goToChat() {
  window.location.href = '/chat';
}
</script>

<style scoped>
.summary-container {
  max-width: 600px;
  margin: 4rem auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  text-align: center;
}
</style>

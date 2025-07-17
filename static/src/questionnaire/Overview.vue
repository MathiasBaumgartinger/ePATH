<template>
  <div>
    <div v-for="(cat, idx) in schema" :key="idx" class="border p-4 mb-4">
      <h2 class="text-lg font-bold">{{ cat.category_title }}</h2>
      <p class="text-sm text-gray-600 mb-2">{{ cat.category_description }}</p>
      <div class="block-progress mb-4">
        <div class="block-progress__inner" :style="{ width: progress[idx].total ? (progress[idx].answered / progress[idx].total * 100) + '%' : '0%' }"></div>
      </div>
      <button class="px-3 py-1 bg-blue-600 text-white rounded" @click="$emit('start', idx)">Continue</button>
    </div>
    <button class="mt-4 px-3 py-1 bg-gray-300 rounded" @click="submitQuestionnaire">Submit Questionnaire</button>
  </div>
</template>

<script setup>
import axios from 'axios'
import { defineProps, defineEmits } from 'vue'
import { useQuestionnaireStore } from './store.js'

// Pinia store for global state
const store = useQuestionnaireStore()

const props = defineProps({
  schema: { type: Array, required: true },
  progress: { type: Array, required: true }
})

function submitQuestionnaire() {
  let postData = store.formData
  // Optionally, you can add any additional data needed for submission
  postData = {
    answers: postData,
    questionnaire_def_fk: store.schemaId, // Assuming schemaId is set in the store
    // TODO: do not hard-code userID
    user_uuid: 1, // Replace with actual user ID logic
    status: store.progress.every(cat => cat.answered === cat.total) ? 'completed' : 'in_progress'
  }
  console.log('Submitting questionnaire data:', postData);
  
  axios.post('/questionnaire/records/', postData)
    .then(response => {
      console.log('Questionnaire submitted successfully:', response.data)
      // Optionally emit an event to notify parent component
      emit('submitted', response.data)
    })
    .catch(error => {
      console.error('Error submitting questionnaire:', error)
      // Handle error appropriately, e.g., show a notification
    })
}
const emit = defineEmits(['start', 'submitted'])
</script>

<style scoped>
.block-progress {
  width: 100%;
  background-color: #e2e8f0;
  border-radius: 0.25rem;
  height: 0.5rem;
  overflow: hidden;
}
.block-progress__inner {
  background-color: #3b82f6;
  height: 100%;
  transition: width 0.3s ease;
}
</style>

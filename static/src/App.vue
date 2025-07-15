<script setup>
import { reactive } from 'vue'
import { QuestionnaireForm } from '@epath/vue-questionnaire'

// Sample schema defining categories and questions
const schema = {
  personal: {
    description: 'Tell us a bit about yourself.',
    questions: {
      name: {
        question: "What's your name?",
        type: 'textarea',
        params: { rows: 2 }
      },
      favorite_color: {
        question: 'What is your favorite color?',
        type: 'radio',
        params: {
          options: [
            { label: 'Red', value: 'red' },
            { label: 'Green', value: 'green' },
            { label: 'Blue', value: 'blue' }
          ]
        }
      }
    }
  }
}

// Reactive object to hold form responses
const formData = reactive({})

// Handle form submission
function handleSubmit(data) {
  console.log('Form submitted:', data)
}
</script>

<template>
  <!-- Pass required props: schema, v-model for formData, and submit handler -->
  <QuestionnaireForm :schema="schema" v-model="formData" @submit="handleSubmit" />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>

<template>
  <div>
    <div class="category-progress mb-2">
      <div class="category-progress__inner" :style="{ width: progress.total ? (progress.answered / progress.total * 100) + '%' : '0%' }"></div>
    </div>
    <p class="text-xs text-gray-700 mb-4">{{ progress.answered }} of {{ progress.total }} answered</p>
    <QuestionnaireForm
      :schema="[category]"
      :model-value="formDataLocal"
      @update:modelValue="next => Object.assign(formDataLocal, next)"
      @progressed="store.setDone"
    />
    <button class="mb-4 px-3 py-1 bg-gray-300 rounded" @click="$emit('back')">Back to Overview</button>
  </div>
</template>

<script setup>
import { reactive, watch, onMounted } from 'vue'
import { QuestionnaireForm } from '@epath/vue-questionnaire'
import { defineProps, defineEmits } from 'vue'
import { useQuestionnaireStore } from './store.js'

const props = defineProps({
  category: { type: Object, required: true },
  progress: {
    type: Object,
    required: true,
    default: () => ({ total: 0, answered: 0 })
  }
})

const emit = defineEmits(['back', 'submit'])

// Pinia store for global state
const store = useQuestionnaireStore()

// Use local reactive form data to isolate category
const formDataLocal = reactive({})

// Initialize local formData from global store when category changes
function initLocal() {
  const categoryKey = props.category.category_title;
  // Clear previous local answers
  Object.keys(formDataLocal).forEach(k => delete formDataLocal[k]);
  // Load stored category data (id -> value)
  const formDataStore = store.formData[categoryKey] || {};
  Object.entries(formDataStore).forEach(([fieldId, val]) => {
    formDataLocal[fieldId] = val;
  });
}
onMounted(initLocal)
watch(() => props.category, initLocal)

watch(formDataLocal, (newData) => {
  // Update the store with local form data  
  store.updateCategoryData(props.category.category_title, newData)
}, { deep: true })
</script>

<style scoped>
.category-progress {
  width: 100%;
  background-color: #e2e8f0;
  height: 0.5rem;
  border-radius: 0.25rem;
  overflow: hidden;
}
.category-progress__inner {
  height: 100%;
  background-color: #3b82f6;
  transition: width 0.3s ease;
}
</style>

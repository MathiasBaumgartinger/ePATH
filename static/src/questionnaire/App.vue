<script setup>
import { onMounted } from 'vue'
import { useQuestionnaireStore } from './store.js'

// initialize Pinia store and fetch questionnaire schema on mount
const store = useQuestionnaireStore()
onMounted(() => store.fetchSchema('AT'))
</script>

<template>
  <!-- Overall progress bar -->
  <div class="overall-progress mb-2">
    <div class="overall-progress__inner"
      :style="{ width: store.overallProgress.total ? (store.overallProgress.answered / store.overallProgress.total * 100) + '%' : '0%' }">
    </div>
  </div>
  <p class="text-xs text-gray-700 mb-4">{{ store.overallProgress.answered }} of {{ store.overallProgress.total }} answered</p>

  <main>
    <!-- Show loading while schema is being fetched -->
    <div v-if="!store.schema.length" class="text-center p-4">Loading questionnaire...</div>
    <RouterView v-else v-slot="{ Component, route }">
      <!-- Render Overview for the main questionnaire route -->
      <component
        v-if="route.name === 'Overview'"
        :is="Component"
        :schema="store.schema"
        :progress="store.progress"
        @start="(idx) => $router.push({ name: 'CategoryView', params: { categoryId: idx } })"
        @submitted="() => $router.push({ name: 'SubmissionSummary' })"
      />
      <!-- Render CategoryView for specific category routes -->
      <component
        v-else
        :is="Component"
        :category="store.schema[route.params.categoryId]"
        :progress="store.progress[route.params.categoryId]"
        @back="() => $router.push({ name: 'Overview' })"
        @submit="(data) => { store.submitCategory(data); $router.push({ name: 'Overview' }) }"
      />
    </RouterView>
  </main>
</template>

<style scoped>
/* Optional: add spacing, typography, etc. */

/* Styled per-block progress bar */
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

/* Overall progress bar styles */
.overall-progress {
  width: 100%;
  background-color: #e2e8f0;
  height: 0.75rem;
  border-radius: 0.375rem;
  overflow: hidden;
}

.overall-progress__inner {
  height: 100%;
  background-color: #10b981;
  transition: width 0.3s ease;
}

/* Category-specific progress bar styles */
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

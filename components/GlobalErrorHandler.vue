<template>
  <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
    <p class="text-red-800 font-semibold">{{ error }}</p>
    <button 
      @click="clearError" 
      class="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
    >
      Dismiss
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const error = ref<string | null>(null)

// Global error handler
const handleError = (err: Error) => {
  console.error('Global Error:', err)
  error.value = err.message || 'An unexpected error occurred'
}

const clearError = () => {
  error.value = null
}

if (process.client) {
  window.addEventListener('error', (event) => {
    handleError(event.error)
  })
}
</script>

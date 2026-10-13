<template>
  <div class="min-h-screen bg-gradient-to-br from-yellow-50 to-amber-100 flex items-center justify-center">
    <div class="text-center max-w-md">
      <div class="mb-8">
        <h1 class="text-9xl font-bold text-amber-600">⚠️</h1>
      </div>

      <h2 class="text-4xl font-bold text-gray-900 mb-4">Oops! An Error Occurred</h2>
      <p class="text-xl text-gray-600 mb-4">{{ error.message || 'Something went wrong' }}</p>
      
      <div v-if="error.statusCode === 404">
        <p class="text-gray-600 mb-8">The page you requested could not be found.</p>
      </div>
      <div v-else-if="error.statusCode === 500">
        <p class="text-gray-600 mb-8">An internal server error occurred. Please try again later.</p>
      </div>
      <div v-else>
        <p class="text-gray-600 mb-8">Please try again or contact support if the problem persists.</p>
      </div>

      <div class="space-y-3">
        <button 
          @click="handleError" 
          class="w-full px-8 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-semibold transition-colors"
        >
          Try Again
        </button>

        <NuxtLink 
          to="/" 
          class="block px-8 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 font-semibold transition-colors"
        >
          Back to Home
        </NuxtLink>
      </div>

      <p class="text-sm text-gray-500 mt-8">Error Code: {{ error.statusCode || 'UNKNOWN' }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps({
  error: {
    type: Object,
    required: true
  }
})

const handleError = () => {
  if (process.server) return
  
  // Clear error and refresh
  clearError({ redirect: '/' })
}
</script>

<style scoped>
/* Error page specific styles */
</style>

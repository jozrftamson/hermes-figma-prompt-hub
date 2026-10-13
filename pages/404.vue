<template>
  <div class="min-h-screen bg-gradient-to-br from-red-50 to-red-100 flex items-center justify-center">
    <div class="text-center">
      <div class="mb-8">
        <h1 class="text-9xl font-bold text-red-600">404</h1>
      </div>

      <h2 class="text-4xl font-bold text-gray-900 mb-4">Page Not Found</h2>
      <p class="text-xl text-gray-600 mb-8">The page you're looking for doesn't exist.</p>

      <div class="space-y-4">
        <NuxtLink 
          to="/" 
          class="inline-block px-8 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-semibold transition-colors"
        >
          Back to Home
        </NuxtLink>

        <div>
          <NuxtLink 
            to="/prompts" 
            class="inline-block ml-4 px-8 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 font-semibold transition-colors"
          >
            View Prompts
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 404 Not Found Page
definePageMeta({
  layout: 'default'
})
</script>

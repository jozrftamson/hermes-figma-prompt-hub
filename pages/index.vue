<template>
  <div class="space-y-8">
    <section class="bg-white rounded-lg shadow p-8">
      <h2 class="text-3xl font-bold mb-4 text-gray-900">Welcome to Hermes Prompt Hub</h2>
      <p class="text-gray-600 text-lg">
        Design, validate, and manage prompts directly from Figma. 
        Seamless integration with your design system.
      </p>
    </section>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-xl font-semibold text-indigo-600 mb-2">📊 Total Prompts</h3>
        <p class="text-4xl font-bold text-gray-900">{{ stats.totalPrompts }}</p>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-xl font-semibold text-indigo-600 mb-2">⭐ Avg Quality</h3>
        <p class="text-4xl font-bold text-gray-900">{{ stats.avgQuality }}%</p>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-xl font-semibold text-indigo-600 mb-2">🔄 Last Sync</h3>
        <p class="text-lg text-gray-600">{{ stats.lastSync }}</p>
      </div>
    </div>

    <section class="bg-white rounded-lg shadow p-8">
      <h3 class="text-2xl font-bold mb-4 text-gray-900">Quick Actions</h3>
      <div class="flex gap-4">
        <NuxtLink 
          to="/prompts/create"
          class="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-semibold"
        >
          Create Prompt
        </NuxtLink>
        <button 
          @click="syncFromFigma"
          class="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 font-semibold"
        >
          Sync from Figma
        </button>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const stats = ref({
  totalPrompts: 5,
  avgQuality: 88,
  lastSync: 'Just now'
})

const syncFromFigma = async () => {
  try {
    await $fetch('/api/figma/sync', { method: 'POST' })
    alert('Sync started from Figma!')
  } catch (err) {
    console.error('Sync failed:', err)
  }
}
</script>

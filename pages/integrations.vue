<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Integrations</h1>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Figma Integration -->
        <section class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center text-2xl">🎨</div>
            <h2 class="text-2xl font-bold text-gray-900">Figma</h2>
          </div>

          <p class="text-gray-600 mb-4">Import prompts directly from Figma frames. Auto-sync changes.</p>

          <div class="mb-6">
            <label class="block text-sm font-semibold text-gray-700 mb-2">File ID</label>
            <input v-model="figmaConfig.fileId" type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500" placeholder="Figma file ID" />
          </div>

          <div class="mb-6">
            <label class="block text-sm font-semibold text-gray-700 mb-2">API Token</label>
            <input v-model="figmaConfig.apiToken" type="password" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500" placeholder="Figma API token" />
          </div>

          <button @click="syncFigma" class="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-semibold">
            Sync from Figma
          </button>
        </section>

        <!-- GitHub Integration -->
        <section class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-12 h-12 bg-gray-800 rounded-lg flex items-center justify-center text-2xl">💻</div>
            <h2 class="text-2xl font-bold text-gray-900">GitHub</h2>
          </div>

          <p class="text-gray-600 mb-4">Connected: jozrftamson/hermes-figma-prompt-hub</p>

          <div class="bg-green-50 border border-green-200 rounded-lg p-3 mb-4">
            <p class="text-sm text-green-800">✓ Repository synced</p>
          </div>

          <button class="w-full px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 font-semibold">
            Push Changes
          </button>
        </section>

        <!-- Vercel Integration -->
        <section class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-12 h-12 bg-black rounded-lg flex items-center justify-center text-2xl">⚡</div>
            <h2 class="text-2xl font-bold text-gray-900">Vercel</h2>
          </div>

          <p class="text-gray-600 mb-4">Auto-deploy from GitHub on every push.</p>

          <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
            <p class="text-sm text-blue-800">✓ Connected & Deploying</p>
          </div>

          <button class="w-full px-4 py-2 bg-black text-white rounded-lg hover:bg-gray-900 font-semibold">
            View Deployment
          </button>
        </section>

        <!-- Validation Integration -->
        <section class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center text-2xl">✓</div>
            <h2 class="text-2xl font-bold text-gray-900">Validation</h2>
          </div>

          <p class="text-gray-600 mb-4">Automatic schema and quality validation on push.</p>

          <div class="bg-green-50 border border-green-200 rounded-lg p-3 mb-4">
            <p class="text-sm text-green-800">✓ All checks passing</p>
          </div>

          <button class="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold">
            View Report
          </button>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const figmaConfig = ref({
  fileId: '',
  apiToken: ''
})

const syncFigma = async () => {
  try {
    await $fetch('/api/figma/sync', {
      method: 'POST',
      body: figmaConfig.value
    })
    alert('Figma sync started!')
  } catch (err) {
    console.error('Sync failed:', err)
    alert('Sync failed')
  }
}
</script>

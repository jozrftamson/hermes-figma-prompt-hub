<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-indigo-600">Hermes Figma Prompt Hub</h1>
          <div class="flex gap-4">
            <NuxtLink to="/" class="text-gray-700 hover:text-indigo-600">Dashboard</NuxtLink>
            <NuxtLink to="/prompts" class="text-gray-700 hover:text-indigo-600">Prompts</NuxtLink>
            <NuxtLink to="/integrations" class="text-gray-700 hover:text-indigo-600">Integrations</NuxtLink>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 py-8">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
// Layout setup
</script>

<style scoped>
/* Layout styles */
</style>

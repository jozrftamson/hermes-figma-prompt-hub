<template>
  <div class="space-y-6">
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-2xl font-bold mb-4 text-gray-900">Prompts Library</h2>
      
      <div class="flex gap-4 mb-6">
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Search prompts..."
          class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <select 
          v-model="selectedCategory"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <option value="">All Categories</option>
          <option value="analysis">Analysis</option>
          <option value="generation">Generation</option>
          <option value="reasoning">Reasoning</option>
        </select>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <NuxtLink
          v-for="prompt in filteredPrompts"
          :key="prompt.prompt_id"
          :to="`/prompts/${prompt.prompt_id}`"
          class="block p-4 border border-gray-200 rounded-lg hover:shadow-lg transition-shadow"
        >
          <h3 class="font-semibold text-lg text-indigo-600 mb-2">{{ prompt.name }}</h3>
          <p class="text-gray-600 text-sm mb-3">{{ prompt.description }}</p>
          <div class="flex gap-2">
            <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-semibold">
              {{ prompt.strategy }}
            </span>
            <span class="px-2 py-1 bg-gray-100 text-gray-800 rounded text-xs font-semibold">
              {{ prompt.category }}
            </span>
          </div>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const prompts = ref([
  {
    prompt_id: 'cot-analysis',
    name: 'Chain of Thought Analysis',
    description: 'Structured step-by-step analysis',
    strategy: 'chain-of-thought',
    category: 'analysis'
  },
  {
    prompt_id: 'few-shot-examples',
    name: 'Few-Shot Learning',
    description: 'Learn from examples',
    strategy: 'few-shot',
    category: 'learning'
  },
  {
    prompt_id: 'role-play',
    name: 'Role Play Persona',
    description: 'Act as expert',
    strategy: 'role-play',
    category: 'behavioral'
  }
])

const searchQuery = ref('')
const selectedCategory = ref('')

const filteredPrompts = computed(() => {
  return prompts.value.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         p.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = selectedCategory.value === '' || p.category === selectedCategory.value
    return matchesSearch && matchesCategory
  })
})
</script>

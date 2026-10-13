<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Evaluations</h1>

      <!-- Filters -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Prompt</label>
            <select v-model="filters.prompt" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="">All Prompts</option>
              <option value="cot-analysis">Chain of Thought</option>
              <option value="few-shot">Few-Shot</option>
              <option value="role-play">Role-Play</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Model</label>
            <select v-model="filters.model" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="">All Models</option>
              <option value="gpt-4">GPT-4</option>
              <option value="gpt-3.5">GPT-3.5 Turbo</option>
              <option value="hermes">Hermes 3</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Date Range</label>
            <select v-model="filters.dateRange" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="7">Last 7 days</option>
              <option value="30">Last 30 days</option>
              <option value="90">Last 90 days</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Evaluations Table -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Prompt</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Model</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Score</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Metrics</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Date</th>
              <th class="px-6 py-3 text-left text-sm font-semibold text-gray-900">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="eval_ in evaluations" :key="eval_.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 text-sm font-medium text-indigo-600">{{ eval_.prompt }}</td>
              <td class="px-6 py-4 text-sm text-gray-900">{{ eval_.model }}</td>
              <td class="px-6 py-4 text-sm">
                <span class="px-3 py-1 rounded-full text-sm font-semibold" :class="getScoreClass(eval_.score)">
                  {{ eval_.score }}/10
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">
                <div class="space-y-1">
                  <p>Clarity: {{ eval_.metrics.clarity }}</p>
                  <p>Completeness: {{ eval_.metrics.completeness }}</p>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ eval_.date }}</td>
              <td class="px-6 py-4 text-sm">
                <button class="text-indigo-600 hover:text-indigo-900 font-semibold">View Details</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const filters = ref({
  prompt: '',
  model: '',
  dateRange: '7'
})

const evaluations = ref([
  {
    id: 1,
    prompt: 'Chain of Thought',
    model: 'GPT-4',
    score: 8.5,
    metrics: { clarity: 0.89, completeness: 0.91 },
    date: '2025-01-16'
  },
  {
    id: 2,
    prompt: 'Chain of Thought',
    model: 'GPT-3.5',
    score: 8.1,
    metrics: { clarity: 0.87, completeness: 0.88 },
    date: '2025-01-16'
  },
  {
    id: 3,
    prompt: 'Few-Shot',
    model: 'GPT-4',
    score: 8.8,
    metrics: { clarity: 0.92, completeness: 0.93 },
    date: '2025-01-15'
  }
])

const getScoreClass = (score: number) => {
  if (score >= 8) return 'bg-green-100 text-green-800'
  if (score >= 7) return 'bg-yellow-100 text-yellow-800'
  return 'bg-red-100 text-red-800'
}
</script>

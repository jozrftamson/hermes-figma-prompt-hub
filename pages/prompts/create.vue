<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Create New Prompt</h1>

      <form @submit.prevent="submitForm" class="bg-white rounded-lg shadow p-8 max-w-2xl">
        <!-- Basic Info -->
        <section class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Basic Information</h2>

          <div class="mb-4">
            <label class="block text-sm font-semibold text-gray-700 mb-2">Prompt ID *</label>
            <input v-model="form.prompt_id" type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="e.g., cot-analysis" required />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-semibold text-gray-700 mb-2">Name *</label>
            <input v-model="form.name" type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Prompt name" required />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-semibold text-gray-700 mb-2">Description *</label>
            <textarea v-model="form.description" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" rows="3" placeholder="Clear description" required></textarea>
          </div>

          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Category *</label>
              <select v-model="form.category" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" required>
                <option value="">Select category</option>
                <option value="analysis">Analysis</option>
                <option value="generation">Generation</option>
                <option value="reasoning">Reasoning</option>
                <option value="classification">Classification</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Strategy *</label>
              <select v-model="form.strategy" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" required>
                <option value="">Select strategy</option>
                <option value="chain-of-thought">Chain of Thought</option>
                <option value="few-shot">Few-Shot</option>
                <option value="role-play">Role-Play</option>
                <option value="tree-of-thought">Tree of Thought</option>
                <option value="meta-reasoning">Meta-Reasoning</option>
              </select>
            </div>
          </div>
        </section>

        <!-- Content -->
        <section class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Content</h2>

          <div class="mb-4">
            <label class="block text-sm font-semibold text-gray-700 mb-2">System Prompt *</label>
            <textarea v-model="form.system" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono text-sm" rows="5" placeholder="System message" required></textarea>
          </div>

          <div class="mb-4">
            <label class="block text-sm font-semibold text-gray-700 mb-2">User Template *</label>
            <textarea v-model="form.user_template" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 font-mono text-sm" rows="5" placeholder="User template with {{variables}}" required></textarea>
          </div>

          <div class="mb-4">
            <label class="block text-sm font-semibold text-gray-700 mb-2">Guardrails (one per line)</label>
            <textarea v-model="form.guardrails_text" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" rows="4" placeholder="Each guardrail on a new line"></textarea>
          </div>
        </section>

        <!-- Actions -->
        <div class="flex gap-4">
          <button type="submit" class="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-semibold">
            Create Prompt
          </button>
          <NuxtLink to="/prompts" class="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 font-semibold">
            Cancel
          </NuxtLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const form = ref({
  prompt_id: '',
  name: '',
  description: '',
  category: '',
  strategy: '',
  system: '',
  user_template: '',
  guardrails_text: ''
})

const submitForm = async () => {
  try {
    const guardrails = form.value.guardrails_text
      .split('\n')
      .map(g => g.trim())
      .filter(g => g.length > 0)

    const promptData = {
      prompt_id: form.value.prompt_id,
      name: form.value.name,
      description: form.value.description,
      version: 'v1',
      category: form.value.category,
      strategy: form.value.strategy,
      system: form.value.system,
      user_template: form.value.user_template,
      guardrails
    }

    await $fetch('/api/prompts', {
      method: 'POST',
      body: promptData
    })

    alert('Prompt created successfully!')
    navigateTo('/prompts')
  } catch (err) {
    console.error('Failed to create prompt:', err)
    alert('Failed to create prompt')
  }
}
</script>

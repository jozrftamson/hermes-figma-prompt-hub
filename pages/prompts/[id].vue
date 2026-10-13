<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 py-6">
        <h1 class="text-3xl font-bold text-indigo-600">Prompt: {{ prompt.name }}</h1>
        <p class="text-gray-600 mt-2">{{ prompt.description }}</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 py-8">
      <div class="grid grid-cols-3 gap-6">
        <!-- Left Column: Prompt Details -->
        <div class="col-span-2 space-y-6">
          <!-- Metadata -->
          <section class="bg-white rounded-lg shadow p-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-4">Metadata</h2>
            <dl class="grid grid-cols-2 gap-4">
              <div>
                <dt class="text-sm font-semibold text-gray-600">Strategy</dt>
                <dd class="text-lg font-medium text-indigo-600">{{ prompt.strategy }}</dd>
              </div>
              <div>
                <dt class="text-sm font-semibold text-gray-600">Category</dt>
                <dd class="text-lg font-medium text-gray-900">{{ prompt.category }}</dd>
              </div>
              <div>
                <dt class="text-sm font-semibold text-gray-600">Version</dt>
                <dd class="text-lg font-medium text-gray-900">{{ prompt.version }}</dd>
              </div>
              <div>
                <dt class="text-sm font-semibold text-gray-600">Quality Score</dt>
                <dd class="text-lg font-medium text-green-600">8.2/10</dd>
              </div>
            </dl>
          </section>

          <!-- System Prompt -->
          <section class="bg-white rounded-lg shadow p-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-4">System Prompt</h2>
            <pre class="bg-gray-100 p-4 rounded text-sm overflow-auto">{{ prompt.system }}</pre>
          </section>

          <!-- User Template -->
          <section class="bg-white rounded-lg shadow p-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-4">User Template</h2>
            <pre class="bg-gray-100 p-4 rounded text-sm overflow-auto">{{ prompt.user_template }}</pre>
          </section>

          <!-- Guardrails -->
          <section class="bg-white rounded-lg shadow p-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-4">Guardrails</h2>
            <ul class="space-y-2">
              <li v-for="(guardrail, idx) in prompt.guardrails" :key="idx" class="flex items-start">
                <span class="text-indigo-600 font-bold mr-3">•</span>
                <span class="text-gray-700">{{ guardrail }}</span>
              </li>
            </ul>
          </section>

          <!-- Examples -->
          <section class="bg-white rounded-lg shadow p-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-4">Examples ({{ prompt.examples.length }})</h2>
            <div class="space-y-4">
              <div v-for="(example, idx) in prompt.examples" :key="idx" class="border border-gray-200 rounded-lg p-4">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <h3 class="font-semibold text-gray-900 mb-2">Input</h3>
                    <pre class="bg-gray-100 p-3 rounded text-sm">{{ example.input }}</pre>
                  </div>
                  <div>
                    <h3 class="font-semibold text-gray-900 mb-2">Output</h3>
                    <pre class="bg-gray-100 p-3 rounded text-sm">{{ example.output }}</pre>
                  </div>
                </div>
                <div v-if="example.explanation" class="mt-3 pt-3 border-t border-gray-200">
                  <h3 class="font-semibold text-gray-900 mb-2">Explanation</h3>
                  <p class="text-gray-700">{{ example.explanation }}</p>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- Right Column: Actions & Info -->
        <div class="col-span-1 space-y-6">
          <!-- Quick Actions -->
          <section class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-bold text-gray-900 mb-4">Actions</h2>
            <div class="space-y-2">
              <button class="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-semibold">
                Test Prompt
              </button>
              <button class="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 font-semibold">
                Run Evaluation
              </button>
              <button class="w-full px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 font-semibold">
                Duplicate
              </button>
              <button class="w-full px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 font-semibold">
                Delete
              </button>
            </div>
          </section>

          <!-- Info Panel -->
          <section class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-bold text-gray-900 mb-4">Info</h2>
            <dl class="space-y-3">
              <div>
                <dt class="text-xs font-semibold text-gray-600 uppercase">Created</dt>
                <dd class="text-sm text-gray-900">2025-01-16</dd>
              </div>
              <div>
                <dt class="text-xs font-semibold text-gray-600 uppercase">Updated</dt>
                <dd class="text-sm text-gray-900">2025-01-16</dd>
              </div>
              <div>
                <dt class="text-xs font-semibold text-gray-600 uppercase">Tokens</dt>
                <dd class="text-sm text-gray-900">1,847</dd>
              </div>
              <div>
                <dt class="text-xs font-semibold text-gray-600 uppercase">Status</dt>
                <dd class="text-sm">
                  <span class="px-2 py-1 bg-green-100 text-green-800 rounded font-semibold">Active</span>
                </dd>
              </div>
            </dl>
          </section>

          <!-- Recent Evaluations -->
          <section class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-bold text-gray-900 mb-4">Recent Evaluations</h2>
            <div class="space-y-2">
              <div class="flex justify-between items-center py-2 border-b">
                <span class="text-sm text-gray-700">GPT-4 Eval</span>
                <span class="text-sm font-semibold text-green-600">8.5/10</span>
              </div>
              <div class="flex justify-between items-center py-2 border-b">
                <span class="text-sm text-gray-700">GPT-3.5 Eval</span>
                <span class="text-sm font-semibold text-green-600">8.1/10</span>
              </div>
              <div class="flex justify-between items-center py-2">
                <span class="text-sm text-gray-700">Hermes 3 Eval</span>
                <span class="text-sm font-semibold text-green-600">7.9/10</span>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const prompt = ref({
  id: 'cot-analysis',
  name: 'Chain of Thought Analysis',
  description: 'Structured step-by-step analysis for complex problems',
  version: 'v1.0',
  strategy: 'chain-of-thought',
  category: 'analysis',
  system: 'You are a step-by-step analytical thinker. Break complex problems into clear, numbered steps. Show your reasoning between each step.',
  user_template: 'Analyze this problem in 5 steps: {{problem}}',
  guardrails: [
    'Each step must be independent and self-contained',
    'Show reasoning between steps, not just conclusions',
    'Validate assumptions at each step',
    'Consider edge cases and alternative interpretations'
  ],
  examples: [
    {
      input: 'Why do users churn from SaaS products?',
      output: '1. Data collection... 2. Trend analysis... 3. Pattern identification...',
      explanation: 'Systematic approach identifying root causes'
    },
    {
      input: 'How to optimize database queries?',
      output: '1. Profile queries... 2. Index analysis... 3. Execution plans...',
      explanation: 'Performance optimization methodology'
    }
  ]
})

onMounted(() => {
  // Load prompt details from API or route params
  console.log('Prompt detail page mounted')
})
</script>

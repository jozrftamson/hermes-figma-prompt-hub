<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Settings</h1>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <!-- Sidebar Navigation -->
        <div class="md:col-span-1">
          <nav class="space-y-2 bg-white rounded-lg shadow p-4">
            <button 
              v-for="tab in tabs" 
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'w-full text-left px-4 py-2 rounded-lg font-semibold transition-colors',
                activeTab === tab.id 
                  ? 'bg-indigo-100 text-indigo-700' 
                  : 'text-gray-700 hover:bg-gray-100'
              ]"
            >
              {{ tab.name }}
            </button>
          </nav>
        </div>

        <!-- Content -->
        <div class="md:col-span-3">
          <!-- Account Settings -->
          <div v-if="activeTab === 'account'" class="bg-white rounded-lg shadow p-6 space-y-6">
            <h2 class="text-2xl font-bold text-gray-900">Account Settings</h2>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Email</label>
              <input type="email" value="user@example.com" class="w-full px-4 py-2 border border-gray-300 rounded-lg" disabled />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Username</label>
              <input type="text" value="jozrftamson" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>

            <button class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-semibold">
              Save Changes
            </button>
          </div>

          <!-- API Keys -->
          <div v-if="activeTab === 'api'" class="bg-white rounded-lg shadow p-6 space-y-6">
            <h2 class="text-2xl font-bold text-gray-900">API Keys</h2>

            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p class="text-sm text-blue-800">Keep your API keys secret. Never share them publicly.</p>
            </div>

            <div class="space-y-4">
              <div v-for="key in apiKeys" :key="key.id" class="flex items-center justify-between border border-gray-200 rounded-lg p-4">
                <div>
                  <p class="font-semibold text-gray-900">{{ key.name }}</p>
                  <p class="text-sm text-gray-600">Created: {{ key.created }}</p>
                </div>
                <button class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-semibold">
                  Revoke
                </button>
              </div>
            </div>

            <button class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-semibold">
              Generate New Key
            </button>
          </div>

          <!-- Notifications -->
          <div v-if="activeTab === 'notifications'" class="bg-white rounded-lg shadow p-6 space-y-6">
            <h2 class="text-2xl font-bold text-gray-900">Notifications</h2>

            <div class="space-y-4">
              <label class="flex items-center">
                <input type="checkbox" checked class="w-4 h-4 text-indigo-600 rounded" />
                <span class="ml-3 text-gray-900">Email on evaluation complete</span>
              </label>

              <label class="flex items-center">
                <input type="checkbox" checked class="w-4 h-4 text-indigo-600 rounded" />
                <span class="ml-3 text-gray-900">Email on Figma sync failure</span>
              </label>

              <label class="flex items-center">
                <input type="checkbox" class="w-4 h-4 text-indigo-600 rounded" />
                <span class="ml-3 text-gray-900">Weekly summary report</span>
              </label>
            </div>

            <button class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-semibold">
              Save Preferences
            </button>
          </div>

          <!-- Integrations -->
          <div v-if="activeTab === 'integrations'" class="bg-white rounded-lg shadow p-6 space-y-6">
            <h2 class="text-2xl font-bold text-gray-900">Connected Integrations</h2>

            <div class="space-y-4">
              <div class="flex items-center justify-between border border-gray-200 rounded-lg p-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">🎨</div>
                  <p class="font-semibold text-gray-900">Figma</p>
                </div>
                <span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold">Connected</span>
              </div>

              <div class="flex items-center justify-between border border-gray-200 rounded-lg p-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center text-white">💻</div>
                  <p class="font-semibold text-gray-900">GitHub</p>
                </div>
                <span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold">Connected</span>
              </div>

              <div class="flex items-center justify-between border border-gray-200 rounded-lg p-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-black rounded-lg flex items-center justify-center text-white">⚡</div>
                  <p class="font-semibold text-gray-900">Vercel</p>
                </div>
                <span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold">Connected</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const tabs = ref([
  { id: 'account', name: 'Account' },
  { id: 'api', name: 'API Keys' },
  { id: 'notifications', name: 'Notifications' },
  { id: 'integrations', name: 'Integrations' }
])

const activeTab = ref('account')

const apiKeys = ref([
  { id: 1, name: 'Production API Key', created: '2025-01-10' },
  { id: 2, name: 'Development API Key', created: '2025-01-15' }
])
</script>

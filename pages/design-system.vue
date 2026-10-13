<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Design System</h1>

      <div class="grid grid-cols-2 gap-6">
        <!-- Colors -->
        <section class="bg-white rounded-lg shadow p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Color Palette</h2>

          <div class="space-y-3">
            <div v-for="color in colors" :key="color.name" class="flex items-center gap-3">
              <div class="w-16 h-10 rounded border" :style="{ backgroundColor: color.hex }"></div>
              <div>
                <p class="font-semibold text-gray-900">{{ color.name }}</p>
                <p class="text-sm text-gray-600">{{ color.hex }}</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Typography -->
        <section class="bg-white rounded-lg shadow p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Typography Scale</h2>

          <div class="space-y-3">
            <div v-for="size in typographySizes" :key="size.name">
              <p :style="{ fontSize: size.size }" class="font-semibold">{{ size.name }}: The quick brown fox</p>
              <p class="text-xs text-gray-600">{{ size.size }} / {{ size.lineHeight }}</p>
            </div>
          </div>
        </section>

        <!-- Spacing -->
        <section class="bg-white rounded-lg shadow p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Spacing Scale</h2>

          <div class="space-y-3">
            <div v-for="space in spacingScale" :key="space.value">
              <p class="text-sm font-semibold text-gray-900 mb-2">{{ space.name }}: {{ space.value }}</p>
              <div class="flex items-end gap-2">
                <div class="bg-indigo-600 rounded" :style="{ width: space.value, height: '24px' }"></div>
              </div>
            </div>
          </div>
        </section>

        <!-- Radius & Shadows -->
        <section class="bg-white rounded-lg shadow p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Radius & Shadows</h2>

          <div class="space-y-4">
            <div>
              <h3 class="font-semibold text-gray-900 mb-3">Border Radius</h3>
              <div class="grid grid-cols-4 gap-2">
                <div v-for="radius in borderRadii" :key="radius.name" class="bg-gray-200 h-20 flex items-center justify-center text-xs font-semibold" :style="{ borderRadius: radius.value }">
                  {{ radius.name }}
                </div>
              </div>
            </div>

            <div>
              <h3 class="font-semibold text-gray-900 mb-3">Shadows</h3>
              <div class="grid grid-cols-3 gap-2">
                <div v-for="shadow in shadowElevations" :key="shadow.name" class="h-20 bg-white rounded" :style="{ boxShadow: shadow.css }">
                  <p class="text-xs font-semibold p-2">{{ shadow.name }}</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- CSS Variables -->
      <section class="bg-white rounded-lg shadow p-6 mt-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">CSS Variables</h2>
        <pre class="bg-gray-100 p-4 rounded overflow-auto text-sm">{{ cssVariables }}</pre>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const colors = ref([
  { name: 'Primary Blue', hex: '#2563EB' },
  { name: 'Secondary Purple', hex: '#A855F7' },
  { name: 'Success Green', hex: '#10B981' },
  { name: 'Warning Amber', hex: '#F59E0B' },
  { name: 'Error Red', hex: '#EF4444' },
  { name: 'Info Cyan', hex: '#0EA5E9' }
])

const typographySizes = ref([
  { name: 'Display', size: '36px', lineHeight: '1.9' },
  { name: 'H1', size: '30px', lineHeight: '1.8' },
  { name: 'H2', size: '24px', lineHeight: '1.7' },
  { name: 'H3', size: '20px', lineHeight: '1.6' },
  { name: 'Body', size: '16px', lineHeight: '1.5' },
  { name: 'Small', size: '14px', lineHeight: '1.4' }
])

const spacingScale = ref([
  { name: 'xs', value: '4px' },
  { name: 'sm', value: '8px' },
  { name: 'md', value: '16px' },
  { name: 'lg', value: '24px' },
  { name: 'xl', value: '32px' },
  { name: '2xl', value: '48px' }
])

const borderRadii = ref([
  { name: 'None', value: '0px' },
  { name: 'SM', value: '2px' },
  { name: 'MD', value: '6px' },
  { name: 'LG', value: '12px' },
  { name: 'XL', value: '16px' },
  { name: 'Full', value: '9999px' }
])

const shadowElevations = ref([
  { name: 'Shadow Base', css: '0 1px 3px rgba(0, 0, 0, 0.1)' },
  { name: 'Shadow MD', css: '0 4px 6px rgba(0, 0, 0, 0.1)' },
  { name: 'Shadow LG', css: '0 10px 15px rgba(0, 0, 0, 0.1)' }
])

const cssVariables = ref(`
:root {
  /* Colors */
  --color-primary: #2563EB;
  --color-secondary: #A855F7;
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #0EA5E9;

  /* Typography */
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 18px;
  --text-xl: 20px;
  --text-2xl: 24px;
  --text-3xl: 30px;
  --text-4xl: 36px;

  /* Spacing */
  --spacing-1: 4px;
  --spacing-2: 8px;
  --spacing-3: 12px;
  --spacing-4: 16px;
  --spacing-5: 20px;
  --spacing-6: 24px;
  --spacing-8: 32px;

  /* Radius */
  --radius-sm: 2px;
  --radius-md: 6px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-base: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1);
}
`)
</script>

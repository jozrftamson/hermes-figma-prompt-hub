<template>
  <button 
    :class="[
      'px-6 py-3 rounded-lg font-semibold transition-colors',
      variantClasses,
      { 'opacity-50 cursor-not-allowed': disabled }
    ]"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  disabled: false
})

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'primary':
      return 'bg-indigo-600 text-white hover:bg-indigo-700'
    case 'secondary':
      return 'bg-gray-200 text-gray-800 hover:bg-gray-300'
    case 'outline':
      return 'border-2 border-indigo-600 text-indigo-600 hover:bg-indigo-50'
    case 'ghost':
      return 'text-gray-700 hover:bg-gray-100'
    default:
      return ''
  }
})
</script>

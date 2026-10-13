<template>
  <div class="bg-gray-100 rounded-lg p-4">
    <p class="text-gray-700">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps({
  message: {
    type: String,
    required: true
  }
})
</script>

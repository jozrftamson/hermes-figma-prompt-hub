<template>
  <div>
    <NuxtRouteAnnouncer />
    <slot />
    <ClientOnly>
      <GlobalErrorHandler />
    </ClientOnly>
  </div>
</template>

<script setup lang="ts">
// App shell component for error handling and global setup
</script>

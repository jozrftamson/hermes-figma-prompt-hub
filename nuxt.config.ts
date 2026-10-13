export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
  ],
  
  ssr: true,
  
  css: [
    '@/assets/styles/global.css',
  ],
  
  components: {
    dirs: [
      {
        path: '@/components',
        prefix: 'App'
      }
    ]
  },
  
  runtimeConfig: {
    figmaApiToken: process.env.FIGMA_API_TOKEN,
    figmaFileId: process.env.FIGMA_FILE_ID,
    figmaTeamId: process.env.FIGMA_TEAM_ID,
    figmaWebhookSecret: process.env.FIGMA_WEBHOOK_SECRET,
  },
  
  typescript: {
    strict: true,
    typeCheck: true,
  },
  
  vite: {
    server: {
      middlewareMode: false,
    }
  }
})

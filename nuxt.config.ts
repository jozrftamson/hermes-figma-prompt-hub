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
    apiBaseUrl: process.env.NUXT_API_BASE_URL || 'http://localhost:3000',
    apiTimeout: process.env.NUXT_API_TIMEOUT || 30000,
    public: {
      figmaFileId: process.env.NUXT_FIGMA_FILE_ID,
      environment: process.env.NUXT_ENV || 'development',
    },
    figmaApiToken: process.env.NUXT_FIGMA_API_TOKEN,
    figmaTeamId: process.env.NUXT_FIGMA_TEAM_ID,
    figmaWebhookSecret: process.env.NUXT_FIGMA_WEBHOOK_SECRET,
  },
  
  typescript: {
    strict: true,
    typeCheck: true,
  },
  
  vite: {
    server: {
      middlewareMode: false,
    }
  },
  
  dev: process.env.NODE_ENV !== 'production',
  
  nitro: {
    prerender: {
      crawlLinks: true,
      routes: ['/sitemap.xml'],
      ignore: ['/admin']
    }
  }
})

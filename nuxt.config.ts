export default defineNuxtConfig({
  modules: [
    '@nuxt/content',
    '@nuxtjs/tailwindcss'
  ],

  content: {
    documentDriven: false
  },

  nitro: {
    prerender: {
      routes: ['/'],
      failOnError: false
    }
  },

  app: {
    head: {
      title: 'Corrèze Travelogue — Tour de France 2026 Stage 9',
      meta: [
        { name: 'description', content: 'A cycling travelogue following the 185km route of Stage 9 of the 2026 Tour de France, from Malemort to Ussel through Corrèze.' }
      ],
      link: [
        { rel: 'stylesheet', href: 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css' }
      ]
    }
  },

  compatibilityDate: '2025-01-01'
})

import { defineCollection, defineContentConfig, z } from '@nuxt/content'

export default defineContentConfig({
  collections: {
    entries: defineCollection({
      type: 'page',
      source: 'entries/**',
      schema: z.object({
        segment: z.number(),
        title: z.string(),
        subtitle: z.string().optional(),
        publishDate: z.string(),
        kmStart: z.number(),
        kmEnd: z.number(),
        gpxFile: z.string().optional().nullable(),
        elevationData: z.string().optional().nullable(),
        images: z.array(z.any()).optional(),
        streetView: z.object({
          embedUrl: z.string(),
          caption: z.string().optional()
        }).optional().nullable(),
        weather: z.any().optional().nullable(),
        draft: z.boolean().default(true)
      })
    })
  }
})

import { defineCollection, defineContentConfig, z } from '@nuxt/content'

export default defineContentConfig({
  collections: {
    entries: defineCollection({
      type: 'page',
      source: 'entries/**',
      schema: z.object({
        // Segment entries carry segment/kmStart/kmEnd; "special" entries
        // (e.g. the July-2 tour-history essay, #502) have none of these and
        // set `special` instead. Keep the segment fields optional so both
        // shapes validate against the one collection.
        segment: z.number().optional(),
        special: z.string().optional(),
        issue: z.number().optional(),
        title: z.string(),
        subtitle: z.string().optional(),
        publishDate: z.string(),
        kmStart: z.number().optional(),
        kmEnd: z.number().optional(),
        gpxFile: z.string().optional().nullable(),
        elevationData: z.string().optional().nullable(),
        images: z.array(z.any()).optional(),
        weather: z.any().optional().nullable(),
        draft: z.boolean().default(true)
      })
    })
  }
})

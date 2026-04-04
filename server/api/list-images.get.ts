import { readdirSync, statSync } from 'fs'
import { resolve, join } from 'path'

export default defineEventHandler(() => {
  const imagesDir = resolve('public/images')
  const images: string[] = []

  function scan(dir: string, prefix: string) {
    try {
      const entries = readdirSync(dir)
      for (const entry of entries) {
        const fullPath = join(dir, entry)
        const stat = statSync(fullPath)
        if (stat.isDirectory()) {
          scan(fullPath, `${prefix}${entry}/`)
        } else if (/\.(jpg|jpeg|png|gif|webp|svg)$/i.test(entry)) {
          images.push(`/images/${prefix}${entry}`)
        }
      }
    } catch {
      // Directory may not exist
    }
  }

  scan(imagesDir, '')
  return { images }
})

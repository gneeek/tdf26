import { execFileSync } from 'child_process'
import { resolve } from 'path'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { segment } = body

  if (!segment && segment !== 0) {
    throw createError({ statusCode: 400, message: 'Missing segment number' })
  }

  if (typeof segment !== 'number' || !Number.isFinite(segment)) {
    throw createError({ statusCode: 400, message: 'segment must be a number' })
  }

  const venvPython = resolve('processing/.venv/bin/python')
  const script = resolve('processing/suggest_images.py')
  const segmentsJson = resolve('data/segments.json')
  const outputDir = resolve('data/image-suggestions')

  try {
    execFileSync(
      venvPython,
      [script, '--segments-json', segmentsJson, '--output-dir', outputDir, '--segment', String(segment)],
      { timeout: 30000, encoding: 'utf8' }
    )
    return { success: true }
  } catch (err: any) {
    throw createError({ statusCode: 500, message: `Suggestion fetch failed: ${err.message}` })
  }
})

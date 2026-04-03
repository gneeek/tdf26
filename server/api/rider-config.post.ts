import { readFileSync, writeFileSync } from 'fs'
import { resolve } from 'path'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { riders, totalDistance, dailyCap, startDate } = body

  if (!riders || !Array.isArray(riders)) {
    throw createError({ statusCode: 400, message: 'Missing or invalid riders array' })
  }

  const configPath = resolve('data/riders/rider-config.json')

  const config = {
    riders,
    totalDistance: totalDistance || 185,
    dailyCap: dailyCap || 2,
    startDate: startDate || '2026-04-01'
  }

  writeFileSync(configPath, JSON.stringify(config, null, 2))

  return { success: true, config }
})
